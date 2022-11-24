import YAML
data = YAML.load_file("data.yml")

@info "Loaded YAML file with $(length(data["cards"])) different cards"

mutable struct Card
    id::String
    quantity::Int
    points::Real
    needs_resources::Dict{String, Int}
    needs_cards::Dict{String, Int}
    provides_resources::Dict{String, Int} 

    needs_expanded::Array{Dict{String, Real}}
end

Quantity = data["game"]["max_cards"]
Safe_Number = 1 / (data["game"]["max_cards"] + 200)

is_a_card(name) = lowercase(name) ∈ lowercase.(keys(data["cards"]))

name_to_id(name) = cards[name].id

generate_identifier(str) = str |>
    s -> replace(s, r"[^a-zA-Z0-9\s]" => "") |>
    split |> 
    s -> first.(s, 4) |>
    s -> lowercase(join(s, "_")) |>
    s -> "int_" * s


function resource_parser(text, default_count::Int)
    # regex101 link:
    # https://regex101.com/r/CExim7/2
    re = r"^(((?<res1>.*?)s?\s+for\s+(?<num1>[0-9]+)\s+(?<parent1>.*?)s?)|((?<num2>[0-9]+)?\s*(?<res2>.*?)s?))(x(?<repeat>[0-9.]+))?$"

    resource = match(re, text)
    if !isnothing(resource[:res1])
        count = isnothing(resource[:num1]) ? default_count : parse(Int, resource[:num1])
        name = lowercase(resource[:res1])
    elseif !isnothing(resource[:res2])
        count = isnothing(resource[:num2]) ? default_count : parse(Int, resource[:num2])
        name = lowercase(resource[:res2])
    else
        @error "Couldn't parse resource" text
    end

    if !isnothing(resource[:repeat])
        count *= parse(Float64, resource[:repeat])
    end

    name, count
end

function yaml_to_card(card_dict, id)
    card_name, card = card_dict

    quantity = "quantity" ∈ keys(card) ? card["quantity"] : 1

    needs_resources = Dict{String, Int}()
    needs_cards = Dict{String, Int}()
    provides_resources = Dict{String, Int}()

    if "needs" ∈ keys(card)
        # Expand compound resources
        to_delete_from_array = []
        for (i, need) ∈ enumerate(card["needs"])
            if !is_a_card(need)
                parsed = resource_parser(need, 1)
                if parsed[1] ∈ keys(data["game"]["resources"])
                    compound_resource = data["game"]["resources"][parsed[1]]
                    push!(to_delete_from_array, i)
                    append!(card["needs"], compound_resource["needs"] .* ("x" * string(parsed[2])))
                end
            end
        end
        deleteat!(card["needs"], to_delete_from_array)
                    
        # Process all resources
        for need ∈ card["needs"]
            if is_a_card(need)
                needs_cards[need] = 1
            else
                name, count = resource_parser(need, -1)
                needs_resources[name] = count
            end
        end
    end

    if "provides" ∈ keys(card)
        for provide ∈ card["provides"]
            name, count = resource_parser(provide, 1)
            provides_resources[name] = count
        end
    end

    card = Card(id, quantity, card["points"], needs_resources, needs_cards, provides_resources, [])

    @debug "Created card $(card)"

    (card_name, card)
end

cards::Dict{String, Card} = Dict( yaml_to_card(card, generate_identifier(card[1])) for (i, card) ∈ enumerate(data["cards"]) )

@info "Cards parsed successfully: " cards

resource_basin::Dict{String, Pair{Dict{String,Real}, Dict{String,Real}}} = Dict()

function add_to_basin_if_not_exists(resource)
    if resource ∉ keys(resource_basin)
        resource_basin[resource] = Pair(Dict(), Dict())
        
        if is_a_card(resource)
            resource_basin[resource][2][resource] = 1 / Safe_Number
        end
    end
end

# Expand needs
for card ∈ cards
    for need ∈ card[2].needs_cards
        # Find the card that's needed
        # TODO: lowercase
        # TODO: 10
        if need[1] ∉ keys(cards)
            @error "Could not find card $(need)"
        else
            push!(card[2].needs_expanded, Dict(cards[need[1]].id => Safe_Number))
            add_to_basin_if_not_exists(need[1])
            resource_basin[need[1]][1][card[1]] = 1
        end
    end

    for resource ∈ card[2].needs_resources
        add_to_basin_if_not_exists(resource[1])
        resource_basin[resource[1]][1][card[1]] = resource[2] < 0 ? Safe_Number : resource[2]

        cards_with_resources = findall(c -> resource[1] ∈ keys(c.provides_resources), cards)

        if isempty(cards_with_resources)
            @error "No card could satisfy $(resource)"
        end

        resource_counts = map(i -> cards[i].provides_resources[resource[1]], cards_with_resources)
        
        resource_counts = Float64.(resource_counts)
        resource_counts = resource[2] ./ resource_counts

        resource_counts[resource_counts .< 0 ] .= Safe_Number

        cards_needed_names = Dict(zip(cards_with_resources, resource_counts))
        @debug "Cards needed to satisfy $(resource[2]) $(titlecase(resource[1]))s for $(card[1]):" cards_needed_names
    end

    for resource ∈ card[2].provides_resources
        add_to_basin_if_not_exists(resource[1])
        resource_basin[resource[1]][2][card[1]] = resource[2]
    end
end

# Sanity check on resource basin
for res ∈ collect(resource_basin)
    name, resource = res
    if isempty(resource[1])
        @warn "No card needs the $(name) resource"
        delete!(resource_basin, name)
    elseif isempty(resource[2])
        @error "There are no cards that provide the $(name) resource"
        delete!(resource_basin, name)
    end
end

@info "Cards expanded successfully" resource_basin

# Equation generation engine (to improve at some point)
quantity_equation = join(map(c -> c.id, values(cards)), " + ") * " <= " * string(data["game"]["max_cards"])

maximise_equation = join(map(c -> string(c.points) * "*" * c.id, values(cards)), " + ")

# intermediates = map(res ->)

resource_equations = map(res -> begin
        lhs = map(c -> string(c[2]) * "*" * name_to_id(c[1]), collect(res[1]))
        rhs = map(c -> string(c[2]) * "*" * name_to_id(c[1]), collect(res[2]))
        join(lhs, " + ") * " <= " * join(rhs, " + ")
    end,
    values(resource_basin)
)



variables = map(c -> string(c.id) * " = 0, >=0, <=" * string(c.quantity), values(cards))

# Put it all together
big_string = "Variables\n" * join(variables, "\n") * "\nEnd Variables\n\nEquations\n" *
    "maximize " * maximise_equation * "\n\n" * quantity_equation * "\n" * join(resource_equations, "\n") *
    "\n" * "End Equations"

@info "Generated APM output"
print(big_string)

open("system.apm", "w") do file
    write(file, big_string)
end
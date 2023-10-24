from gekko import GEKKO

m = GEKKO(remote=False)
m.options.SOLVER=1
m.solver_options = ['minlp_maximum_iterations 40000', 'minlp_max_iter_with_int_sol 40000']
m.solver_options = ['minlp_maximum_iterations 40000', 'minlp_max_iter_with_int_sol 40000']


#%% Variables

int_part_dete = m.Var(value=0 , lb=0 , ub=2 , integer=True , name='int_part_dete')
int_samp_retu = m.Var(value=0 , lb=0 , ub=1 , integer=True , name='int_samp_retu')
int_came = m.Var(value=0 , lb=0 , ub=2 , integer=True , name='int_came')
int_livi_quar_l = m.Var(value=0 , lb=0 , ub=3 , integer=True , name='int_livi_quar_l')
int_kitc = m.Var(value=0 , lb=0 , ub=1 , integer=True , name='int_kitc')
int_eva = m.Var(value=0 , lb=0 , ub=1 , integer=True , name='int_eva')
int_labo_l = m.Var(value=0 , lb=0 , ub=2 , integer=True , name='int_labo_l')
int_gym = m.Var(value=0 , lb=0 , ub=1 , integer=True , name='int_gym')
int_sola_pane = m.Var(value=0 , lb=0 , ub=4 , integer=True , name='int_sola_pane')
int_biol_expe = m.Var(value=0 , lb=0 , ub=2 , integer=True , name='int_biol_expe')
int_rtg = m.Var(value=0 , lb=0 , ub=1 , integer=True , name='int_rtg')
int_fuel_tank_s = m.Var(value=0 , lb=0 , ub=4 , integer=True , name='int_fuel_tank_s')
int_robo_arm = m.Var(value=0 , lb=0 , ub=1 , integer=True , name='int_robo_arm')
int_nurs = m.Var(value=0 , lb=0 , ub=1 , integer=True , name='int_nurs')
int_labo_s = m.Var(value=0 , lb=0 , ub=3 , integer=True , name='int_labo_s')
int_atmo_sens = m.Var(value=0 , lb=0 , ub=2 , integer=True , name='int_atmo_sens')
int_batt_liio = m.Var(value=0 , lb=0 , ub=3 , integer=True , name='int_batt_liio')
int_magn = m.Var(value=0 , lb=0 , ub=2 , integer=True , name='int_magn')
int_ante_rota = m.Var(value=0 , lb=0 , ub=1 , integer=True , name='int_ante_rota')
int_ante_stat = m.Var(value=0 , lb=0 , ub=1 , integer=True , name='int_ante_stat')
int_livi_quar_s = m.Var(value=0 , lb=0 , ub=3 , integer=True , name='int_livi_quar_s')
int_batt_nicd = m.Var(value=0 , lb=0 , ub=4 , integer=True , name='int_batt_nicd')
int_fuel_tank_l = m.Var(value=0 , lb=0 , ub=2 , integer=True , name='int_fuel_tank_l')

#%% End Variables



#%% Intermediates

harbor = m.Intermediate(40*int_samp_retu,'harbor')
w = m.Intermediate(400*int_sola_pane+800*int_rtg,'w')
gb = m.Intermediate(800*int_ante_rota+800*int_ante_stat,'gb')
bed = m.Intermediate(2*int_livi_quar_l+1*int_livi_quar_s,'bed')
sport = m.Intermediate(40*int_livi_quar_l+40*int_livi_quar_s,'sport')
l = m.Intermediate(400*int_fuel_tank_s+2000*int_fuel_tank_l,'l')
food = m.Intermediate(40*int_kitc,'food')
wh = m.Intermediate(600*int_batt_liio+200*int_batt_nicd,'wh')
price = m.Intermediate(200*int_part_dete+100*int_came+1000*int_livi_quar_l+4000*int_kitc+10000*int_eva+5000*int_labo_l+500*int_gym+600*int_sola_pane+5000*int_biol_expe+20000*int_rtg+400*int_fuel_tank_s+20000*int_robo_arm+3000*int_nurs+2000*int_labo_s+200*int_atmo_sens+500*int_batt_liio+10*int_magn+30*int_ante_rota+20*int_ante_stat+500*int_livi_quar_s+100*int_batt_nicd+2500*int_fuel_tank_l,'price')
xperience = m.Intermediate((2.0*int_labo_l+1.0*int_labo_s+1)*(7*int_part_dete+3*int_came+3*int_eva+2*int_gym+5*int_biol_expe+1*int_robo_arm+4*int_nurs+6*int_atmo_sens+4*int_magn),'xperience')

#%% End Intermediates



#%% Equations

m.Obj(-((2.0*int_labo_l+1.0*int_labo_s+1)*(7*int_part_dete+3*int_came+3*int_eva+2*int_gym+5*int_biol_expe+1*int_robo_arm+4*int_nurs+6*int_atmo_sens+4*int_magn)))

m.Equation(int_part_dete*1+int_samp_retu*0+int_came*1+int_livi_quar_l*1+int_kitc*1+int_eva*1+int_labo_l*1+int_gym*1+int_sola_pane*1+int_biol_expe*1+int_rtg*1+int_fuel_tank_s*1+int_robo_arm*1+int_nurs*1+int_labo_s*1+int_atmo_sens*1+int_batt_liio*1+int_magn*1+int_ante_rota*1+int_ante_stat*1+int_livi_quar_s*1+int_batt_nicd*1+int_fuel_tank_l*1<=15)
m.Equation(1*int_labo_s+1*int_eva+3*int_labo_l+1*int_nurs<=harbor)
m.Equation(300*int_part_dete+50*int_came+50*int_livi_quar_l+100*int_kitc+300*int_labo_l+30*int_gym+40*int_biol_expe+200*int_nurs+150*int_labo_s+150*int_robo_arm+200*int_atmo_sens+20*int_magn+90*int_ante_rota+60*int_ante_stat+30*int_livi_quar_s<=w)
m.Equation(10*int_gym+300*int_part_dete+50*int_biol_expe+300*int_atmo_sens+600*int_came+200*int_magn+10*int_eva+10*int_robo_arm+10*int_nurs<=gb)
m.Equation(1*int_labo_s+1*int_eva+3*int_labo_l+1*int_nurs<=bed)
m.Equation(1*int_gym<=sport)
m.Equation(10*int_part_dete+2000*int_samp_retu+10*int_atmo_sens+40*int_ante_rota+200*int_ante_stat+200*int_robo_arm+2000<=l)
m.Equation(1*int_labo_s+1*int_eva+3*int_labo_l+1*int_nurs<=food)
m.Equation(400*int_sola_pane<=wh)

#%% End Equations


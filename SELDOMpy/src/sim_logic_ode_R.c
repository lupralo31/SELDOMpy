
#include <stdlib.h>
#include <Rinternals.h>
#include <string.h>
#include <include_amigo/AMIGO_model.h>
#include <include_amigo/AMIGO_problem.h>

int amigoRHS(realtype t, N_Vector y, N_Vector ydot, void *data);

void amigoRHS_get_OBS(void* data);

void amigoRHS_get_sens_OBS(void* data);

void amigo_Y_at_tcon(void* amigo_model, realtype t, N_Vector y);

AMIGO_model* R_AMIGOmodelAlloc(SEXP model, SEXP exps, SEXP ivpsol,int exp_num);

int getListElement (SEXP list, char *str);

SEXP simulation_task(AMIGO_problem* amigo_problem,SEXP model,SEXP exps,SEXP ivpsol);

SEXP sim_obs_task(AMIGO_problem* amigo_problem,SEXP model,SEXP exps,SEXP ivpsol);

SEXP sim_logic_ode(SEXP model,SEXP exps,SEXP ivpsol,SEXP task){
  
  AMIGO_problem* amigo_problem;
  AMIGO_model** amigo_models;
  SEXP res;
  int elm1,i,n_exp;
  int n = length(exps);

  n_exp=n;

  amigo_models=(AMIGO_model**)malloc(sizeof(AMIGO_model*)*n_exp);

  for (i = 0; i < n_exp; i++){
  	amigo_models[i]=R_AMIGOmodelAlloc(model,exps,ivpsol,i);
	}
  
  amigo_problem=allocate_AMIGO_problem(n_exp,amigo_models);
  
  set_AMIGO_problem_rhs(amigo_problem,amigoRHS,amigo_Y_at_tcon);
	set_AMIGO_problem_obs_function(amigo_problem,amigoRHS_get_OBS,amigoRHS_get_sens_OBS);
  
  elm1=getListElement(model,"nthreads");
  if(elm1>=0) amigo_problem->nthreads=INTEGER(VECTOR_ELT(model,elm1))[0];
  else error("ERROR nthreads must be defined in model");
  
  if(strcmp(CHAR(STRING_ELT(task, 0)),"sim_CVODES_ODE")==0){
    res=simulation_task(amigo_problem,model,exps,ivpsol);
  }else if(strcmp(CHAR(STRING_ELT(task, 0)),"OBS_CVODES_ODE")==0){
    res=sim_obs_task(amigo_problem,model,exps,ivpsol);
  }else{
    error("A valid task must be provided");
  }
  
  free_AMIGO_problem(amigo_problem);
  
  return(res);

}

AMIGO_model* R_AMIGOmodelAlloc(SEXP model, SEXP exps, SEXP ivpsol,int exp_num){
  
  AMIGO_model* amigo_model;
  SEXP exp;
  
  int elm1;
  int n_states,n_observables,n_pars,n_opt_pars,n_times,n_opt_ics,n_controls,n_controls_t,i,j,counter;  

  exp=VECTOR_ELT(exps, exp_num);
  
  elm1=getListElement(model,"n_states");
  if(elm1>=0) n_states=INTEGER(VECTOR_ELT(model,elm1))[0];
  else error("ERROR");
  
  
  elm1=getListElement(exp,"n_observables");
  if(elm1>=0) n_observables=INTEGER(VECTOR_ELT(exp,elm1))[0];
  else error("ERROR");
  
  elm1=getListElement(model,"x");
  if(elm1>=0) n_pars=length(VECTOR_ELT(model,elm1));
  else error("ERROR");
  
  elm1=getListElement(exp,"t_s");
  if(elm1>=0) n_times=length(VECTOR_ELT(exp,elm1));
  else error("ERROR");
  
  elm1=getListElement(model,"n_stimuli");
  if(elm1>=0) n_controls=INTEGER(VECTOR_ELT(model,elm1))[0];
  else error("ERROR");
  
  elm1=getListElement(exp,"t_con");
  if(elm1>=0)  n_controls_t=length(VECTOR_ELT(exp,elm1));
  else error("ERROR");
  
  n_opt_pars=0;  
  n_opt_ics=0;
  
  amigo_model=allocate_AMIGO_model(n_states,n_observables,n_pars,
  	n_opt_pars,n_times,n_opt_ics,n_controls, n_controls_t,exp_num);


 //index_observables
  elm1=getListElement(exp,"index_observables");
  if(elm1>=0) ;
  else error("ERROR field index_observables must exist");
  
	
	if(length(VECTOR_ELT(exp,elm1))<n_observables){

		amigo_model->use_obs_func=1;
		amigo_model->use_sens_obs_func=1;

	}else{
    
    for (i = 0; i < length(VECTOR_ELT(exp,elm1)); i++)
      amigo_model->index_observables[i]=INTEGER(VECTOR_ELT(exp,elm1))[i]-1;
	}
	
	//Simulation Pars
  elm1=getListElement(model,"x");
  if(elm1>=0);
  else error("ERROR field pars ust exist in model");
	
	for (i = 0; i < n_pars; i++){
		amigo_model->pars[i]=REAL(VECTOR_ELT(model,elm1))[i];
	}
  
  //initial simulation times
	elm1=getListElement(exp,"t_0");
  if(elm1>=0) ;
  else error("ERROR field t_0 must exist in experimental definition");
	amigo_model->t0=REAL(VECTOR_ELT(exp,elm1))[0];
  
  //initial simulation times
  elm1=getListElement(exp,"t_f");
  if(elm1>=0) ;
  else error("ERROR field t_f must exist in experimental definition");
	amigo_model->tf=REAL(VECTOR_ELT(exp,elm1))[0];
  
  //Sampling times
  elm1=getListElement(exp,"t_s");
  if(elm1>=0) ;
  else error("ERROR field t_s must exist in experimental definition");
	for (i = 0; i < n_times; i++){
		amigo_model->t[i]=REAL(VECTOR_ELT(exp,elm1))[i];
	}
  
  //Initial conditions
  elm1=getListElement(exp,"y0");
  if(elm1>=0) ;
  else error("ERROR field y0 must exist in experimental definition");
  for (i = 0; i < n_states; i++){
		amigo_model->y0[i]=REAL(VECTOR_ELT(exp,elm1))[i];
	}
   
   //Control times	
  elm1=getListElement(exp,"t_con");
  if(elm1>=0) ;
  else error("ERROR field t_con must exist in experimental definition");
	for (i = 0; i <n_controls_t; i++){
		amigo_model->controls_t[i]=REAL(VECTOR_ELT(exp,elm1))[i];
	}
  
  //Control values
  counter=0;
  elm1=getListElement(exp,"u");
  if(elm1>=0) ;
  else error("ERROR field u must exist in experimental definition");
	for (i = 0; i < n_controls; i++) {
		for (j= 0; j < n_controls_t-1; j++){
			amigo_model->controls_v[i][j]=REAL(VECTOR_ELT(exp,elm1))[counter++];
      //Rprintf("control_i%d_j%d=%f\n",i,j,amigo_model->controls_v[i][j]);
		}
    
	}
  
 //Experimental data
	counter=0;
  elm1=getListElement(exp,"exp_data");
  if(elm1>=0) ;
  else error("Experimental data  field must exist in experimental definition");
	if (n_observables>0){
		for (i = 0; i < n_observables; i++){
			for (j = 0; j < n_times; j++){
				amigo_model->exp_data[i][j]=REAL(VECTOR_ELT(exp,elm1))[counter++];
			}
		}
  }
  
  //Simulation Related Parameter
	//rtol
  elm1=getListElement(ivpsol,"rtol");
  if(elm1>=0) ;
  else error("rtol field must exist in experimental definition");
  amigo_model->reltol=REAL(VECTOR_ELT(ivpsol,elm1))[0];
  
  //atol
  elm1=getListElement(ivpsol,"atol");
  if(elm1>=0) ;
  else error("atol field must exist in experimental definition");
  amigo_model->atol=REAL(VECTOR_ELT(ivpsol,elm1))[0];

  //max_step_size
  elm1=getListElement(ivpsol,"max_step_size");
  if(elm1>=0) ;
  else error("max_step_size field must exist in experimental definition");
  amigo_model->max_step_size=REAL(VECTOR_ELT(ivpsol,elm1))[0];
	
	//max_num_steps
  elm1=getListElement(ivpsol,"max_num_steps");
  if(elm1>=0) ;
  else error("max_num_steps field must exist in experimental definition");
  amigo_model->max_num_steps=INTEGER(VECTOR_ELT(ivpsol,elm1))[0];
  
  //max_error_test_fails
  elm1=getListElement(ivpsol,"max_error_test_fails");
  if(elm1>=0) ;
  else error("max_error_test_fails field must exist in experimental definition");
  amigo_model->max_error_test_fails=INTEGER(VECTOR_ELT(ivpsol,elm1))[0];
  
  return(amigo_model);
  
}


SEXP simulation_task(AMIGO_problem* amigo_problem,SEXP model,SEXP exps,SEXP ivpsol){
  
  SEXP out,sim,costf,tats;
  int i,j,k,elm1, counter=0;
  double cost;
  int count=0;
  
  cost=eval_AMIGO_problem_LSQ(amigo_problem);
 
  out=PROTECT(allocVector(REALSXP,1));

  if(isnan(cost)){
    REAL(out)[0]=R_PosInf;
  }else if(cost>=DBL_MAX){
    REAL(out)[0]=R_PosInf;  
  }else{
    REAL(out)[0]=cost;  
  }

  UNPROTECT(1);
  
  return(out);
  
}

SEXP sim_obs_task(AMIGO_problem* amigo_problem,SEXP model,SEXP exps,SEXP ivpsol){
  
  SEXP obs,sim,costf,tats;
  int i,j,k,elm1, counter=0,count_prot=0;
  
  SEXP out=PROTECT(allocVector(VECSXP,amigo_problem->n_models));
  count_prot++;
  
  eval_AMIGO_problem_LSQ(amigo_problem);
 
  for (i = 0; i < amigo_problem->n_models; ++i) {
    
    PROTECT(obs=allocMatrix(REALSXP, amigo_problem->amigo_models[i]->n_times, amigo_problem->amigo_models[i]->n_states));
    count_prot++;
    
    counter=0;
    for (j = 0; j < amigo_problem->amigo_models[i]->n_observables; ++j) {
      for (k = 0; k < amigo_problem->amigo_models[i]->n_times; ++k) {
        REAL(obs)[k +  amigo_problem->amigo_models[i]->n_times * j]=amigo_problem->amigo_models[i]->obs_results[j][k];
      }
    }
    
    SET_VECTOR_ELT(out, i, obs);
    
  }
  
  UNPROTECT(count_prot);
  
  return(out);

}


int getListElement (SEXP list, char *str){
  
  SEXP names = getAttrib(list, R_NamesSymbol);
  int i;
  
  for (i = 0; i < length(list); i++)
    if(strcmp(CHAR(STRING_ELT(names, i)), str) == 0) {
      return(i);
    }

    return(-1);
}
 
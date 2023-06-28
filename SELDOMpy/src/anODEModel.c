#include <amigoRHS.h>
#include <math.h>
#include <amigoJAC.h>
#include <amigoSensRHS.h>

//#define inhibitor(i)



/* Right hand side of the system (f(t,x,p))*/
int amigoRHS(realtype t, N_Vector y, N_Vector ydot, void *data){
    AMIGO_model* amigo_model=(AMIGO_model*)data;

    
    int n_states, n_inputs;
    
    double inhibitor,x,k,n,w,tau;
    int i,j,m,n_minterms;
    int ind,ind2;
    int counter=0;
    int input;
    int dec;
    int countBin=0;
    int vecBin[300];
    double resprod;
    double ressum;
    
    
    double fHill[30];
    
    
    n_states=amigo_model->n_states;
    
    for(i = 0; i < n_states; i++){
        //
        n_inputs=(int)amigo_model->pars[counter++];
        if(n_inputs>0){
            
            for(j = 0; j < n_inputs; j++){
                
                input=(int)amigo_model->pars[counter++];
                k=amigo_model->pars[counter++];
                n=amigo_model->pars[counter++];
                //printf ("input = %d k = %f n = %f n_states = %d ith= %f x = %f \n", input, k , n, n_states, Ith(y,i), Ith(y,input));
                if(input==-1){
                    fHill[j]=1;
                }else if(input==-2){
                    fHill[j]=0;
                }else{
                  
                    x=Ith(y,input);
                    fHill[j]=(pow(x,n)/(pow(x,n)+pow(k,n)))*(1+pow(k,n));
                }
            }
            
            ressum=0;
            n_minterms=(int)pow(2,n_inputs);
            
            for(ind = 0; ind < n_minterms; ind++){
                //mexPrintf("n_mini=%d j=%d\n",n_minterms,ind);
                dec=ind;
                resprod=1;
                
                for(m=n_inputs-1;m>=0;m--){
                    vecBin[m]=(int)dec%2;
                    dec=(int)dec/2;
                    //mexPrintf("m=%d\n",m);
                }
                
                for(ind2 = 0; ind2 < n_inputs; ind2++){
                    
                    if(vecBin[ind2]){
                        resprod*=fHill[ind2];
                    }else{
                        resprod*=(1-fHill[ind2]);
                    }
                    // mexPrintf("%d ",vecBin[ind2]);
                    
                }
                //mexPrintf("\n");
                //mexPrintf("\nind=%d\n",ind);
                
                w=amigo_model->pars[counter++];
                ///mexPrintf("w=%e\n",w);
                ressum+=resprod*w;
                
            }
         
            tau=amigo_model->pars[counter++];
            
            inhibitor=(*amigo_model).controls_v[i][0];
            //if(inhibitor>0)Rprintf("Exp n=%d state_num=%d  inhhibitor=%f\n",amigo_model->exp_num,i,inhibitor);
            //Rprintf("Exp n=%d state_num=%d  inhhibitor=%f\n",amigo_model->exp_num,i,inhibitor);
            Ith(ydot,i)=(ressum-Ith(y,i))*tau*(1-inhibitor);
            
            
        }else{
            tau=amigo_model->pars[counter++];
            Ith(ydot,i)=0;
            
        }
        
    }
    

    return(0);
    
}
void amigoRHS_get_sens_OBS(void* data){
    
}

void amigoRHS_get_OBS(void* data){
    
}

void amigo_Y_at_tcon(void* data, realtype t, N_Vector y){
    AMIGO_model* amigo_model=(AMIGO_model*)data;
    
}

#include<stdlib.h>
#include<stdio.h>
#include<time.h>

//int initiator[2][2] = { {0, 1} , {1 , 1}};
static int **temp_matrix; 
static int **crnt_matrix;
static int **initiator;


void create_kronecker(int order)
{
	int i,j,k, jj, kk, tempjj, tempkk;
	int new_order = 2*order;

	if(order >= 4096)
		return;

	//Create a 2d graph of order 2n
	crnt_matrix = (int**)malloc(new_order * sizeof(int*));
	for(i=0;i<new_order; i++){
		crnt_matrix[i] = (int*)malloc(new_order * sizeof(int));
	}

	for(jj=0; jj < new_order; jj += 2){
		for(kk=0; kk < new_order; kk += 2){
			tempjj = jj / 2;
			tempkk = kk / 2;
			if(temp_matrix[tempjj][tempkk] == 1){
				for(j = jj; j< jj + 2; j++){
					for(k = kk; k < kk + 2 ; k++){
						crnt_matrix[j][k] = initiator[j%2][k%2];	
					}
				}
			}
			else{
				for(j = jj; j< jj + 2; j++){
					for(k = kk; k < kk + 2 ; k++){
						crnt_matrix[j][k] = 0;	
					}
				}
			}
		}
	}

/*
	for(i=0;i<new_order;i++){
		for(j=0;j<new_order;j++){
			printf("%d\t", crnt_matrix[i][j]);
		}
		printf("\n");
	}

	for(i=0;i<new_order; i++){
		free(crnt_matrix[i]);
	}
*/
	temp_matrix = crnt_matrix;
	create_kronecker(new_order);
}

int prob_edge(int prob)
{
	static int seed = 1;
	srand(seed++);
	int temp = rand() % 10 + 1;
	if(temp / 10 <= prob)
		return 1;
	else
		return 0;
}

int main()
{
	//temp_matrix = initiator;
	int i,j;
	initiator = (int**)malloc(2 * sizeof(int*));
	for(i=0;i<2; i++){
		initiator[i] = (int*)malloc(2 * sizeof(int));
	}
	initiator[0][0] = 0;
	initiator[0][1] = initiator[1][0] = initiator[1][1] = 1;
	temp_matrix = initiator;

	create_kronecker(2);


	for(i=0;i<4096;i++){
		for(j=0;j<4096;j++){
			if(temp_matrix[i][j] == 1)
				printf("%d\t%d\n", i, j);
		}
	}
	
	return 0;
}



#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

struct edge{
	int from;
	int to;
	struct edge* next;
}; 						

struct myGraph{
	unsigned int binary;
	unsigned long int in;
	unsigned long int out;
	unsigned long int allIn;
	unsigned long int allOut;
};

struct region{
	unsigned long int binary;
	struct region* next;
};

// IMPORTANT VARIABLES AND STRUCTURES

struct edge* increments; // list that will contain the edges' increments
struct myGraph* graph; // graph's array
struct region* regions; // regions' list
int numNodes = 0;
int numInt = 0;

// FUNCTIONS

void readFile(FILE* f); // function that will read the GRAPH from the file
void buildIncrement(int from, int to); // function that will populate the increments' list
void superFree(void); // frees all dynamically allocated structures
void initializeGraph(void);  // function that initializes the structures
void printGraph(void); // function that prints the GRAPH
bool increment(void); // function that will increment the number of edges' on the GRAPH
void detectCycle(int from, int to);
void propagate(int from);

int main(void){	
	FILE* fin; 
	fin = fopen("graph3.txt", "rt");
	
	readFile(fin);
	fclose(fin);
	
	while(increment());
	
	printf("\nNumero de iteracoes : %d \n", numInt);	
//	printGraph();
	
	return(0);
}

void readFile(FILE* f){
	int from, to;
	
	fscanf(f, "%d", &numNodes); // reading the number of nodes
	
	initializeGraph();
	
	while(fscanf(f, "%d %d", &from, &to) != EOF)
		buildIncrement(from, to);
}

void initializeGraph(void){
	int i;
	increments = NULL;
	graph = NULL;
	regions = NULL;
	
	graph = (struct myGraph*) malloc ((numNodes + 1) * sizeof(struct myGraph));
	graph[1].binary = 1;
	
	for(i = 1; i <= numNodes; i++){
		graph[i].in = 0;
		graph[i].out = 0;
		graph[i].allIn = 0;
		graph[i].allOut = 0;
	}
		
	
	for(i = 2; i <= numNodes; i++){
		graph[i].binary = graph[i - 1].binary * 2;
//		printf("graph[%d] = %d\n", i, graph[i].binary);
	}
}

void superFree(void){
	free(graph);
}

void buildIncrement(int from, int to){
	struct edge* newEdge;
	struct edge* aux;
	aux = increments;	
	
	if(increments != NULL)
		while(aux -> next != NULL)
			aux = aux -> next;
	
	regions = (struct region*) malloc (sizeof(struct region));
	regions -> binary = 0;
	regions -> next = NULL;
	newEdge = (struct edge*) malloc (sizeof(struct edge));
	newEdge -> from = from;
	newEdge -> to = to;
	newEdge -> next = NULL;
	
	if(increments != NULL)
		aux -> next = newEdge;
	else
		increments = newEdge;
}

void printGraph(void){
	int i, j;
	
	for(i = 1; i <= numNodes; i++)
		for(j = 1; j <= numNodes; j++)
			if((graph[i].out & graph[j].binary) == graph[j].binary)
				printf("%d > %d\n", i, j);	
		
}

bool increment(void){
	if(increments == NULL)
		return false;
	
	detectCycle(increments -> from, increments -> to); 
	
	struct edge* aux2;
	aux2 = increments;
	increments = increments -> next;
	free(aux2);
	
	return true;
}

void detectCycle(int from, int to){
	struct region* aux;
	struct region* pointerRegionFrom;
	struct region* pointerRegionTo;
	struct region* zero;
	bool boolTo = false;
	bool boolFrom = false;
	
	printf("\n%d > %d\n", from, to);
	
	pointerRegionFrom = NULL;
	pointerRegionTo = NULL;

	if(regions -> binary == 0){
		regions -> binary = regions -> binary | graph[from].binary | graph[to].binary; // on the first increment, we add the two nodes composing the edge to the first region
	
		aux = (struct region*) malloc (sizeof(struct region));
		aux -> binary = 0;
		aux -> next = NULL;
		regions -> next = aux;
	}
	
	aux = regions;
	
	while(aux -> next != NULL){ // searching for the region the two nodes are at
		if((aux -> binary & graph[from].binary) == graph[from].binary)		
			pointerRegionFrom = aux;
		
		if((aux -> binary & graph[to].binary) == graph[to].binary)
			pointerRegionTo = aux;
			
		if(aux -> binary == 0)
			zero = aux;
			
		aux = aux -> next;
	}
	
	if(aux -> binary == 0){ // creating the new region
		struct region* newRegion;
		newRegion = (struct region*) malloc (sizeof(struct region));
		newRegion -> binary = 0;
		newRegion -> next = NULL;
		
		if(pointerRegionFrom == NULL){
			aux -> binary = graph[from].binary;
			boolFrom = true;
		}
		if(pointerRegionFrom == NULL && pointerRegionTo == NULL){
			aux -> binary = aux -> binary | graph[to].binary;
			pointerRegionFrom = aux;
			pointerRegionTo = aux;
			boolTo = true;
		}
		
		aux -> next = newRegion;
	}
	
	if(pointerRegionFrom -> binary != pointerRegionTo -> binary){	
		numInt++;
		printf("Deu ruim !\n");
		
		pointerRegionFrom -> binary = pointerRegionFrom -> binary | pointerRegionTo -> binary; // uniting "from" and "to" into "from"
		pointerRegionTo -> binary = 0;
		
		if(aux -> binary == 0 && aux -> next == NULL && zero -> next == NULL){ // transforming "to" into the new zero
			aux = NULL;
			zero = pointerRegionTo;
		}
		
		// CONTINUAR!
	}else{
		graph[to].in = graph[to].in | graph[from].binary; // to <- from
		graph[from].out = graph[from].out | graph[to].binary; // from -> to
		
		graph[to].allIn = graph[to].allIn | graph[from].allIn; // A -> from -> to ==> A -> to
		graph[to].allOut = graph[to].allOut | graph[from].allIn; // to -> B ==> from -> B
		
		graph[to].allIn = graph[to].allIn | graph[to].in; // Ancestral(to) = non-reachable_Neighbor(to)
		graph[from].allOut = graph[from].allOut | graph[from].out; // Descendant(from) = Neighbor(from)	
	}
	
	if((graph[to].allIn & graph[to].binary) == graph[to].binary){ // if "to" belongs to Reaches(to) ==> to -> * -> to (there is a cycle)
		printf("Ciclo detectado! : ");
		numInt++;
		graph[to].allIn = graph[to].allIn & (!graph[to].binary); // removing "to" from Reaches(to)
		
		if(from == to)
			printf("%d > %d", to, from);
		
	}else if((graph[to].out & graph[from].binary) == graph[from].binary && (graph[from].out & graph[to].binary) == graph[to].binary){ // from -> to ^ to -> from ==> there is a cycle
		printf("Ciclo detectado! : ");
		numInt++;
		printf("%d > %d > %d", to, from, to);
	}
}

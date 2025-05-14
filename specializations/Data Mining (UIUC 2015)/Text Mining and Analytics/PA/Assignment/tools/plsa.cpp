/**
 * @file plsa.cpp
 * @author Hussein Hazimeh
 *
 * Note: This code is not efficient (especially in space)
 * We are using it just for demonstration purposes. 
 * If you want to implement an efficient version of PLSA, you 
 * should avoid storing P(z_{d,w} = j), which can be done by
 * combining the E and M steps.
 */

#include <iostream>
#include <vector>
#include <map>
#include "index/inverted_index.h"
#include "index/forward_index.h"
#include "index/postings_data.h"
#include <random>
#include <cmath>
using namespace meta;

/*
In all what follows, we use:
	The integer d to loop over documents
	The integer w to loop over words
	The integer j to loop over topics
*/

class PLSA{
private:
	std::vector<std::vector<std::vector<double>>> Pz; // Pz[d][w][j] = P(z_{d,w} = j)
	std::vector<std::vector<double>> PzB; // PzB[d][w] = P(z_{d,w} = B)
	std::vector<std::vector<double>> pi; // pi[d][j] = pi_{d,j}
	std::vector<std::vector<double>> Pw; // Pw[j][w] = P(w|theta_j)
	std::vector<double> PB; // PB[w] = P(w|theta_B)
	std::vector<std::vector<int>> Counts; // Counts[d][w] = c(w,d)
	std::shared_ptr<index::inverted_index> idx; // Pointer to the inverted index
	double lambda_B; // Coefficient that controls the proportion of background words
	
	int iterations; // Number of iterations before termination
	int num_topics; // Number of topics k
	int num_docs; // Number of documents in the corpus
	int num_words; // Number of words in the vocabulary

	bool submission; // Ignore this
	std::map<int,int> inverse_term_index; // Ignore this
	double seed; // Ignore (seed for the pseudo-random number generator)

public:
	PLSA(std::shared_ptr<index::inverted_index> index, std::map<int,int>& inv_term_index, std::vector<std::vector<int>>& C, std::vector<double>& PCollection, int k, int iters, double lambda, double random_seed, bool submit); // Constructor
	void Estep();
	void Mstep();
	void Iterate(); // Keeps calling the E and M steps until the required number of iterations is reached.
	void PrintLikelihood(int i);
	void PrintTopics();
	void Submit();
};

// This is the function that you should complete
void PLSA::Estep()
{
	// Implementation of equation (10)
	for (int d=0; d<num_docs; ++d) // Loop over documents
	{
		for (int w=0; w<num_words; ++w) // Loop over words
		{
			double denominator = 0; // Denominator of equation (10)
			for (int j=0; j<num_topics;++j) // Loop over topics and calculate the numerator for each topic
			{
				Pz[d][w][j] = pi[d][j] * Pw[j][w]; // Numerator of equation (10)
				denominator += Pz[d][w][j];
			}

			if (denominator ==0) {denominator = 10e-40;} // Ignore this (avoids division by zero)
			for (int j=0; j<num_topics;++j) // Normalize the numerator of each topic
				Pz[d][w][j] = Pz[d][w][j]/denominator;
		}
	}

	// Incomplete implementation of equation (11). This is where you should complete the code.
	for (int d=0; d<num_docs; ++d) // Loop over documents
	{
		for (int w=0; w<num_words; ++w) // Loop over words
		{
			/*
			Calculate the numerator and denominator of equation (11)
			You can use "for (int j=0; j<num_topics;++j)" to loop over topics
			Do not worry about division by zero in the denominator
			Insert your code after this comment
			*/




			PzB[d][w] = 0; // Change 0 to the correct value, i.e. numerator/denominator
			// You should not insert or change any code after this line
		}
	}
}



void PLSA::Mstep()
{
	// Implementation of equation (12)
	for (int d=0;d<num_docs;++d) // Loop over documents
	{
		double denominator = 0; // Denominator of equation (12)
		for (int j=0;j<num_topics;++j) // Loop over topics
		{
			double numerator = 0; // Numerator of equation (12)
			for (int w=0;w<num_words;++w) // Loop over words
				numerator += Counts[d][w]*(1-PzB[d][w])*Pz[d][w][j];
			pi[d][j] = numerator;
			denominator += numerator;
		}
		if (denominator ==0) {denominator = 10e-40;} // Ignore this (avoids division by zero)
		for (int j=0;j<num_topics;++j) // Normalize the numerator of each mixing weight
			pi[d][j] = pi[d][j]/denominator;

	}

	// Implementation of equation (13)
	for (int j=0;j<num_topics;++j) // Loop over topics
	{
		double denominator = 0; // Denominator of equation (13)
		for (int w=0;w<num_words;++w) // Loop over words
		{
			double numerator = 0; // Numerator of equation (13)
			for (int d=0;d<num_docs;++d) // Loop over documents
				numerator += Counts[d][w]*(1-PzB[d][w])*Pz[d][w][j];
			Pw[j][w] = numerator;
			denominator += numerator;
		}
		if (denominator ==0) {denominator = 10e-40;} // Ignore this (avoids division by zero)
		for (int w=0;w<num_words;++w) // Normalize the numerator of each P(w|theta_j)
			Pw[j][w] = Pw[j][w]/denominator;
	}
}

// You can ignore the code after this line


void PLSA::Iterate()
{
	for (int i=0;i<iterations;++i)
	{
		Estep();
		Mstep();
		if (!submission)
			PrintLikelihood(i);
	}
	if (!submission)
		PrintTopics();
	else
		Submit();
}

void PLSA::PrintLikelihood(int i)
{
	double loglikelihood = 0;
	for (int d=0;d<num_docs;++d)
	{
		for (int w=0;w<num_words;++w)
		{
			double sum = 0;
			for (int j=0;j<num_topics;++j)
				sum += pi[d][j]*Pw[j][w];
			loglikelihood += Counts[d][w] * log(lambda_B*PB[w]+(1-lambda_B)*sum);
		}
	}
	std::cout<<"Iteration: "<<i<<". Log-Likelihood= "<<loglikelihood<<std::endl;
}

void PLSA::PrintTopics()
{
	for (int i=0;i<num_topics;++i)
	{
		std::vector<size_t> indices(num_words);
		for (int j = 0; j < num_words; ++j) 
			indices[j] = j;
		std::sort(indices.begin(), indices.end(), [&](size_t x, size_t y) {return Pw[i][x] > Pw[i][y];});
		std::cout<<printing::make_bold("============================")<<std::endl;
		std::cout<<printing::make_bold("Topic: ")<<i+1<<std::endl;
		for (int j=0;j<20;++j)
			std::cout<<idx->term_text(inverse_term_index[indices[j]])<<" "<<Pw[i][indices[j]]<<std::endl;
	}
}

// Constructor
PLSA::PLSA(std::shared_ptr<index::inverted_index> index, std::map<int,int>& inv_term_index, std::vector<std::vector<int>>& C, std::vector<double>& PCollection, int k, int iters, double lambda, double random_seed, bool submit)
{
	idx = index;
	num_topics = k;
	iterations = iters;
	lambda_B = lambda;
	seed = random_seed;
	PB = PCollection;
	Counts = C;
	inverse_term_index = inv_term_index;
	num_docs = Counts.size();
	num_words = Counts[0].size();
	submission = submit;

	Pz.resize(num_docs);
	for (int i=0;i<num_docs;++i)
	{
		Pz[i].resize(num_words);
		for (int j=0;j<num_words;++j)
			Pz[i][j].resize(num_topics);
	}

	PzB.resize(num_docs);
	for (int i=0;i<num_docs;++i)
		PzB[i].resize(num_words);

	std::random_device rd;
	std::mt19937 mt(seed);
	std::uniform_real_distribution<double> dist(1,1000);
	pi.resize(num_docs);
	for (int i=0;i<num_docs;++i)
	{
		pi[i].resize(num_topics);
    	double total = 0;
		for (int j=0;j<num_topics;++j)
		{
			if (!submission)
				pi[i][j] = dist(mt);
			else
				pi[i][j] = i+j; // Use non-random initialization in case of submission
			total += pi[i][j];
		}
		for (int j=0;j<num_topics;++j)
			pi[i][j] = pi[i][j]/total;
	}

	Pw.resize(num_topics);
	for (int i=0;i<num_topics;++i)
	{
		Pw[i].resize(num_words);
    	double total = 0;
		for (int j=0;j<num_words;++j)
		{
			if (!submission)
				Pw[i][j] = dist(mt);
			else
				Pw[i][j] = i+j;
			total += Pw[i][j];
		}
		for (int j=0;j<num_words;++j)
			Pw[i][j] = Pw[i][j]/total;
	}

}

void PLSA::Submit()
{
	std::ofstream submission;
    submission.open("Assignment/plsa.txt");
    if (!submission.is_open())
        std::cout<<"Problem writing the output to the system. Make sure the program has enough writing privileges."<<std::endl;
	for (int i=0;i<num_topics;++i)
	{
		std::vector<size_t> indices(num_words);
		for (int j = 0; j < num_words; ++j) 
			indices[j] = j;
		std::sort(indices.begin(), indices.end(), [&](size_t x, size_t y) {return Pw[i][x] > Pw[i][y];});
		for (int j=0;j<20;++j)
			submission<<idx->term_text(inverse_term_index[indices[j]])<<" "<<Pw[i][indices[j]]<<std::endl;
	}
	submission.close();
}

int main(int argc, char* argv[])
{
    if (argc != 10 && argc!= 3)
    {
        std::cerr << "Error: Usage:\t" << argv[0] << " configFile " << "--topics " << "--lambda " << "--iter " << "--seed" << std::endl;
        return 1;
    }

    int i=2;
    int k=2;
    int iter=20;
    double seed=6;
    double lambda=0.8;
    while (argc!=3 && i<argc)
    {
    	try
    	{
	    	if(std::strcmp(argv[i],"--topics")==0) {k=std::atoi(argv[i+1]);i+=2;}
	    	else if (std::strcmp(argv[i],"--lambda")==0) {lambda=std::atof(argv[i+1]);i+=2;}
	    	else if (std::strcmp(argv[i],"--iter")==0) {iter=std::atoi(argv[i+1]);i+=2;}
	    	else if (std::strcmp(argv[i],"--seed")==0) {seed=std::atof(argv[i+1]);i+=2;}
	    	else throw 1;
    	}
    	catch(...)
    	{
    		std::cerr << "Error: Usage:\t" << argv[0] << " configFile " << "--topics " << "--lambda " << "--iter " << "--seed" << std::endl;
    		return 1;
    	}
    }

    if (argc == 3 && !(std::strcmp(argv[2],"--submission")==0) )
    {
    	std::cerr << "Error: Usage:\t" << argv[0] << " configFile " << "submission"<<std::endl;
    	return 1;
    }


    auto idx = index::make_index<index::dblru_inverted_index>(argv[1], 30000); // Inverted Index

    auto fidx = meta::index::make_index<index::memory_forward_index>(argv[1]); // Forward Index

    std::map<int,int> term_index;
    std::map<int,int> inverse_term_index;
    int j = 0;

    // Ignore all terms that appear in only one document (for efficiency purposes)
    for (size_t i=0;i<idx->unique_terms();++i)
    {
    	if (idx->total_num_occurences(i) > 1)
    	{
    		term_index[i] = j;
    		inverse_term_index[j] = i;
    		j++;
    	}
    }

    std::vector<std::vector<int>> C(idx->num_docs());
    for (size_t i=0;i<idx->num_docs();++i)
    {
    	C[i].resize(j);
    	auto postings_list = fidx->index::forward_index::search_primary(i)->counts();
    	for (auto& pair: postings_list)
    	{
    		if (term_index.count(pair.first) == 1)
    			C[i][term_index[pair.first]] = pair.second;
    	}
    }
    
    std::vector<double> PCollection(j);
    double total_counts = 0;
    for (size_t i=0;i<PCollection.size();++i){
    	PCollection[i] = double(idx->total_num_occurences(inverse_term_index[i]));
    	total_counts += PCollection[i];
    }

    for (size_t i=0;i<PCollection.size();++i){
    	PCollection[i] = PCollection[i]/total_counts;
    }


    PLSA X(idx, inverse_term_index, C, PCollection, k, iter, lambda, seed, argc==3);
    X.Iterate();
    return 0;
}
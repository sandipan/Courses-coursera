/**
 * @file association.cpp
 * @author Hussein Hazimeh
 */

#include <iostream>
#include <vector>
#include <tuple>
#include "index/postings_data.h"
#include "index/inverted_index.h"
using namespace meta;

// Below is the function that you should complete
double MutualInformation(int Na, int Nb, int Nab, int N)
{
	/*
	Na is the document frequency of word a
	Nb is the document frequency of word b
	Nab is the number of documents that contain both words
	N is the number of documents in the collection
	*/
	double PXa1 = (Na+0.5)/(N+1); // P(Xw_{a} = 1)
	double PXb1 = (Nb+0.5)/(N+1); // P(Xw_{b} = 1)
	double PXa0 = 1-PXa1; // P(Xw_{a} = 0)
	double PXb0 = 1-PXb1; // P(Xw_{b} = 0)
	double PXab11 = (Nab+0.25)/(N+1); // P(Xw_{a} = 1, Xw_{b} = 1)

	double PXab01 = 0; // Replace 0 with the correct formula
	double PXab10 = 0; // Replace 0 with the correct formula
	double PXab00 = 0; // Replace 0 with the correct formula
	return 0; // Replace 0 with the correct formula - Use the function log2() for implementing the logarithm
	// You should not insert or modify any code after this line
}


// You can safely ignore the code below this point (feel free to go through it)
struct compare  
{  
	bool operator()(const std::tuple<double,int,int> l, const std::tuple<double,int,int> r)  
	{  
	   return std::get<0>(l)>std::get<0>(r);
	}  
};  

/*
The function top_terms uses a priority queue that maintains the k word pairs
with the highest co-occurrence (MI =0) or mutual information (MI=1).
The queue has the lowest value at the head; Every new value (co-occurrence or MI) 
is compared to the value at the head. If it is larger, then the head is popped 
and the new value is pushed to the queue.
*/
std::priority_queue<std::tuple<double,int,int>, std::vector<std::tuple<double,int,int>>, compare> top_terms(std::shared_ptr<index::inverted_index> idx, bool MI, size_t num_terms)
{
	std::priority_queue<std::tuple<double,int,int>, std::vector<std::tuple<double,int,int>>, compare> A;
	for (size_t i=0;i<idx->unique_terms();++i) // Loop over first word in the pair
	{
		if(idx->doc_freq(i)>20) // Ignore words with document frequency below 20
		{
			auto postings_list1 = idx->search_primary(i)->counts(); // Extract the documents that have the first term
			for (size_t j=i+1;j<idx->unique_terms();++j) // Loop over second word in the pair
			{
				if(idx->doc_freq(j)>20) // Ignore words with document frequency below 20
				{
					auto postings_list2 = idx->search_primary(j)->counts(); // Extract the documents that have the second term
					int num_occurences = 0; // Number of co-occurrences of the pair (i,j)
					// Take the intersection of the two postings lists. The size of the intersection is the number of co-occurrences.
					for (auto& pair1: postings_list1)
						for (auto& pair2: postings_list2)
							if (pair1.first == pair2.first)
							{
								num_occurences += 1;
								break;
							}
					double score;
					if (MI == 1)
						score = MutualInformation(idx->doc_freq(i),idx->doc_freq(j),num_occurences,idx->num_docs());
					else
						score = static_cast<double>(num_occurences);
					if (A.size()==num_terms && score>std::get<0>(A.top()))
					{
						std::tuple<double,int,int> v(score,i,j);
						A.pop();
						A.push(v);
					}
					else if (A.size()<num_terms)
					{	std::tuple<double,int,int> v(score,i,j);
						A.push(v);
					}
				}
			}
		}
	}
	return A;
}





int main(int argc, char* argv[])
{
	if (argc < 2 || argc>5)
    {
        std::cerr << "Error: Usage:\t" << argv[0] << " configFile " << "--words " << "(--MI) " <<std::endl;
        return 1;
    }

	std::ofstream submission;
    size_t num_words = 20;
    bool MI = 0;
    bool submit = 0;
    int i = 2;

    while (i<argc)
    {
    	try
    	{
	    	if(std::strcmp(argv[i],"--words")==0) {num_words=std::atoi(argv[i+1]);i+=2;}
	    	else if (std::strcmp(argv[i],"--MI")==0) {MI = 1;i+=1;}
	    	else if (std::strcmp(argv[i],"--submission")==0) 
	    	{
	    		submit=1;MI=1;i+=1;
   				submission.open("Assignment/mutual-information.txt");
   				if (!submission.is_open())
       				std::cout<<"Problem writing the output to the system. Make sure the program has enough writing privileges."<<std::endl;
	    	}
	    	else throw 1;
    	}
    	catch(...)
    	{
    		std::cerr << "Error: Usage:\t" << argv[0] << " configFile " << "--words " << "(--MI) " <<std::endl;
    		return 1;
    	}
    }

	auto idx = index::make_index<index::dblru_inverted_index>(argv[1], 30000);
	auto N = top_terms(idx, MI, num_words);
	std::vector<std::tuple<double,int,int>> v(N.size());
	size_t j=N.size()-1;

	while(!N.empty())
	{
		v[j] = N.top();
		--j;
		N.pop();
	}

	if (!submit)
		for(size_t j=0;j<v.size();++j)
			std::cout<<std::get<0>(v[j])<<" "<<idx->term_text(std::get<1>(v[j]))<<" "<<idx->term_text(std::get<2>(v[j]))<<std::endl;

	else
	{
		for(size_t j=0;j<v.size();++j)
				submission<<std::get<0>(v[j])<<" "<<idx->term_text(std::get<1>(v[j]))<<" "<<idx->term_text(std::get<2>(v[j]))<<std::endl;
		submission.close();
	}

	return 1;
}
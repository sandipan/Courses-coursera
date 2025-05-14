/**
 * @file competition.cpp
 * @author Hussein Hazimeh
 */

#include <iostream>
#include <string>
#include <vector>
#include "caching/all.h"
#include "classify/classifier/all.h"
#include "classify/loss/all.h"
#include "index/forward_index.h"
using namespace meta;

int main(int argc, char* argv[])
{
    if (argc != 2)
    {
        std::cout << "Usage:\t" << argv[0] << " config.toml" << std::endl;
        return 1;
    }


    std::ofstream submission;
    submission.open("Assignment/competition.txt");
    if (!submission.is_open())
    {
        std::cout<<"Problem writing the output to the system. Make sure the program has enough writing privileges. Quiting..."<<std::endl;
        return 0;
    }
    std::string nickname;
    std::cout<<"Enter your nickname: ";
    std::getline(std::cin,nickname);
    submission<<nickname+'\n'; // Add the nickname to the first line in the output file



	auto fidx = meta::index::make_index<index::memory_forward_index>(argv[1]); // Pointer to the forward index

	auto config = cpptoml::parse_file(argv[1]);

	auto class_config = config.get_table("classifier"); // Read the classifier type from config.toml
	auto classifier = meta::classify::make_classifier(*class_config, fidx); // Pointer to the classifier

	std::vector<doc_id> train; // stores the document ids of the 546 training documents
	std::vector<doc_id> test; // stores the document ids of the 200 testing documents
	int i=0;
	for (auto& v: fidx->docs())
	{
		if (i<=545)
			train.push_back(v);
		else
			test.push_back(v);
		i++;
	}

	classifier->train(train); // Train the classifier on the training data (first 546 documents)
	auto confusion_mtrx = classifier->test(train); // Create the confusion matrix for the training data
	std::cout<<"Below are the statistics on the training data: "<<std::endl;
	confusion_mtrx.print();
	confusion_mtrx.print_stats();


	for (auto& doc : test) // Loop over the testing document IDs (i.e. the last 200)
		submission<<classifier->classify(doc)<<'\n'; // Classify each document and print its label to file

	submission.close();
    return 0;
}
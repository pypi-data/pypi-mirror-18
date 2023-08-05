﻿#include "ParameterTestSystem.h"

#include "factory.hpp"


std::string ParameterTestSystem::getDocs(){
    return std::string(
"System used to test parameter inputs\n\n"
);
}

ParameterTestSystem::ParameterTestSystem(void)
{
    INPUT(parameter_vector, "Parameter vector")
    INPUT(parameter_matrix, "Parameter Matrix")
    INPUT(parameter_map, "Parameter Map")

    OUTPUT(output_from_vector, "Value of first element in parameter_vector")
    OUTPUT(output_from_matrix, "Value of first column, first row in parameter_matrix")
    OUTPUT(output_from_map, "Value of element 'a' in parameter_map")

}

void ParameterTestSystem::doStep(double time){
    output_from_vector = parameter_vector[0];
    output_from_matrix = parameter_matrix[0][0];
    output_from_map = parameter_map["a"];
}

REGISTER_SYSTEM(ParameterTestSystem);

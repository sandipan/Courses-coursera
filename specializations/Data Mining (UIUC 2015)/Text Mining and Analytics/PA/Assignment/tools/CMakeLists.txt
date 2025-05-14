add_executable(profile profile.cpp)
target_link_libraries(profile meta-index
                              meta-greedy-tagger
                              meta-parser
                              ${CMAKE_THREAD_LIBS_INIT})

add_executable(plsa plsa.cpp)
target_link_libraries(plsa meta-index)

add_executable(association association.cpp)
target_link_libraries(association meta-index)

add_executable(competition competition.cpp)
target_link_libraries(competition meta-classify
                               	     meta-index)

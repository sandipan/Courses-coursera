#!/bin/bash

# 1. Create bash_workdir
mkdir -p bash_workdir

# 2. Redirect standard output to output_bash.txt
exec > bash_workdir/output_bash.txt

# 3. Copy data.txt to bash_workdir
cp data.txt bash_workdir/

# 4. Change into bash_workdir and print the current path
cd bash_workdir
pwd

# 5. Create first_var and print it
first_var="I love HPC!"
echo $first_var

# 6. Use grep to find instances of 80 in data.txt
grep 80 data.txt

# 7. Store the list of files in second_var and print each value
second_var=$(ls)

for file in $second_var
do
    echo $file
done

# 8. Copy output_bash.txt back to projects/week1-bash
cp output_bash.txt ..

# 9. Change back to projects/week1-bash
cd ..

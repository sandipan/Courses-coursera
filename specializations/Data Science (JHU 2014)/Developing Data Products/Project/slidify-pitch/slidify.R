setwd("C:/Users/SANDIPAN DEY/Desktop/coursera/Developing Data Products/Project/slidify-pitch//sandipan.github.io")
library(slidify)
author("final_deck")
slidify("index.Rmd")
git clone https://github.com/sandipan/sandipan.github.io
cd sandipan.github.io
git checkout --orphan gh-pages
git add --all
git commit -a -m "master commit"
git push origin gh-pages
#publish(user="sandipan", repo="sandipan.github.io")
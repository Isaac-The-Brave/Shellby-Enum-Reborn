go install github.com/hakluke/hakrawler@latest
sudo mv ~/go/bin/hakrawler /bin/

go get github.com/Emoe/kxss
sudo mv ~/go/bin/kxss /bin/

go get -u github.com/tomnomnom/gf
sudo mv ~/go/bin/gf /bin/
cd ~
mkdir .gf
cd .gf
git clone https://github.com/Isaac-The-Brave/GF-Patterns-Redux
mv GF-Patterns-Redux/*.json .
rm -rf GF-Patterns-Redux

sudo snap install waybackpy

go install github.com/hahwul/dalfox/v2@latest
sudo mv ~/go/bin/dalfox /bin/

go install github.com/tomnomnom/qsreplace@latest
sudo mv ~/go/bin/qsreplace /bin/

pip install -r requirements.txt
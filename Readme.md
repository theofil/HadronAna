Heppy code, adapted from Riccardo Manzoni

<h4> LXPLUS instructions (20 November 2018) </h4>

```
setenv SCRAM_ARCH slc6_amd64_gcc630
cmsrel CMSSW_9_4_6_patch1
cd CMSSW_9_4_6_patch1/src 
cmsenv
git cms-init
git remote add cmg-central https://github.com/CERN-PH-CMG/cmg-cmssw.git  -f  -t heppy_94X_dev
cp /afs/cern.ch/user/c/cmgtools/public/sparse-checkout_94X_heppy .git/info/sparse-checkout
git checkout -b heppy_94X_dev cmg-central/heppy_94X_dev
git remote add origin git@github.com:theofil/cmg-cmssw.git
git push -u origin heppy_94X_dev
git clone -o cmg-central https://github.com/CERN-PH-CMG/cmgtools-lite.git -b 94X_dev CMGTools
cd CMGTools 
git remote add origin git@github.com:theofil/cmgtools-lite.git
git push -u origin 94X_dev
```

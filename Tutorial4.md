# Tutorial 4 Plan

## Working with the VM(Download, ssh, scp)

### SSH

```
ssh csc309@192.168.58.128
```

password = pass (Note you can setup ssh keys https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-2 if you want to)

### Copy directory to remote
```
scp -r csc309@192.168.58.128:{path in remote} {path to local file} 
```

### Copy directory to remote
```
scp -r {path to local file} csc309@192.168.58.128:{path in remote}
```

Even better, use VSCode Remote SSH/Equivalent extension/feature of your IDEs to remotely mount the file


## Downloading virtualenv(already installed on the vm), downloading Django on virtualenv

### Requires python, pip

```
pip install virtualenv

virtualenv {envname}

source {envname}/bin/activate

pip install django

```
### Notes

- make sure you are currently at the same directory that you ran virtualenv in) 


### Windows specific issues

- You might not be able to call `virtualenv {envname}` directly, instead use `python3 -m virtualenv {envname}`


## Assignment feedback (css portion + explaining some html autotester issues)

## More in-depth models, admin view(chat demo)


## Google slides reference

https://docs.google.com/presentation/d/1XxJL41qaeOQG3Fp2_YyuKv0rdgIcCOmuMsc7ajQFTMw/edit#slide=id.g113293c4b31_0_29

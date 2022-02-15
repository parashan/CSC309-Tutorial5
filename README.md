# Tutorial 4 notes

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

### SSH Tunnel to allow browser connection to localhost while running server on VM

```
ssh -L 8000:127.0.0.1:8000 csc309@192.168.58.128
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







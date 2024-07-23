### Run sentiment as a systemd service

```bash
(cd ../;make quadlet)
sudo cp ../build/sentiment.yaml ../build/sentiment.kube ../build/sentiment.image /usr/share/containers/systemd/
sudo /usr/libexec/podman/quadlet --dryrun #optional
sudo systemctl daemon-reload
sudo systemctl start sentiment
```

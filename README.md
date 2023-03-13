## Setup
Copy the whole folder to the raspberry.

On the raspberry.
```bash
sudo -i
cd /home/pi/XP_TV
```

Install pip
```bash
sudo apt install -y python3-pip libxslt1-dev
```

Install packages
```bash
pip install -r requirements.txt
```

Copy systemd service to `/lib/systemd/system/`
```bash
cp xp_tv.service /lib/systemd/system/
```

Start and enable the service
```bash
systemctl start xp_tv.service
systemctl enable xp_tv.service
systemctl status xp_tv.service
```
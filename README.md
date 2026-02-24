1. Clone the Repo

git clone https://github.com/chrishuber11/vault_os
cd vault_os

2. Create Virtual Environment

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Make startup script executable

chmod +x system/startup.sh

4. Install systemd user service

mkdir -p ~/.config/systemd/user
cp system/fallout.service ~/.config/systemd/user/

5. Reload systemd

systemctl --user daemon-reload

6. Enable auto-start

systemctl --user enable fallout.service

7. Allow user services to run without login

loginctl enable-linger $USER

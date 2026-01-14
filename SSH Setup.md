# Remote Access Setup: Mac ↔ Linux Mint (SSH + Tailscale)

This document explains how to set up a Linux Mint machine as a server, connect to it from a MacBook via SSH, copy files, and extend access using **Tailscale** for remote connectivity.

---

## 1. Install and Enable SSH on Linux Mint
```bash
sudo apt update
sudo apt install openssh-server -y
sudo systemctl enable ssh
sudo systemctl start ssh
systemctl status ssh
```
Make sure it shows **active (running)**.

---

## 2. Find the Linux Mint IP Address
On Mint:
```bash
ip -4 a | grep inet
```

On Mac: 

```bash
ifconfig | grep -Eo 'inet ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)' | awk '{print $2}'
```

- Example output:  

  ```
  wlo1: inet 172.20.10.2/28
  ```
- Here, the Mint machine IP is **`172.20.10.2`**.

---

## 3. Connect via SSH from Mac
On Mac (outside SSH session):
```bash
ssh name@172.20.10.2
```
Replace `name` with your Mint username. Enter the password when prompted.

→ if you don't know the username you can type: 

```bash
whoami
```

→ Debugging Connection: 

```bash
ping 192.168.1.12
ssh -vvv abdulrahim@192.168.1.12
```

---

## 4. Copy Files with `scp`
Run these commands **on your Mac** (not inside SSH):

### Copy file from Mint → Mac:
```bash
scp gemy@172.20.10.2:/home/gemy/Desktop/odooinstal.sh ~/Desktop/
```

### Copy folder from Mint → Mac:
```bash
scp -r gemy@172.20.10.2:/home/gemy/Desktop/myfolder ~/Desktop/
```

### Copy file from Mac → Mint:
```bash
scp ~/Desktop/somefile.txt gemy@172.20.10.2:/home/gemy/Desktop/
```

→ Quote the entire path if there's spaces

```shell
scp -r gemy@172.20.10.2:"/home/gemy/Desktop/my folder" "~/Desktop/my destination/"
```

→ Copy to Odoo.sh

```shell
rsync -av \
"/Users/ahmed/Desktop/test to live/import_contacts.py" \
26769158@capstone-solution-bubblzz-testdb-26769158.dev.odoo.com:/home/odoo/
```



---

## 5. GUI Drag-and-Drop (Termius)
- Install **Termius** on Mac.  
- Add your Linux Mint machine using IP (`172.20.10.2`), username, and password.  
- Supports drag-and-drop file transfers. ✅

---

## 6. Remote Access Beyond Local Network (Tailscale)
To connect when machines are on **different networks** (not the same Wi-Fi/hotspot):

### Install Tailscale on Linux Mint:
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```
- Sign in with your Google/GitHub/Microsoft account.

### Install Tailscale on Mac:
- Download & install from: [https://tailscale.com/download](https://tailscale.com/download)
- Sign in with the **same account**.

### Check Tailscale IP on Mint:
```bash
tailscale ip -4
```
Example: `100.x.y.z`

### Connect from Mac (anywhere!):
```bash
ssh gemy@100.x.y.z
```

---

## 7. Notes
- On iPhone hotspot, IP looked like `172.20.10.x` (private network). Both devices must be connected to the same hotspot for direct SSH.  
- With **Tailscale**, you can SSH into Mint from anywhere, even across different networks.  
- Tailscale **Free Plan**:  
  - Up to 3 users  
  - Up to 100 devices  
  - Unlimited data transfer  
  - Features like Tailscale SSH & MagicDNS  

---

## 8. Useful Commands
- Exit SSH:
  ```bash
  exit
  ```
- Exit SFTP shell:
  ```bash
  exit
  # or
  bye
  ```
- Check Tailscale status:
  ```bash
  tailscale status
  ```

EC2 Instance

1. Launch an EC2 Instance
 - Go to AWS Console → EC2 → Launch Instance
 - Choose Amazon Linux 2 or Ubuntu (Ubuntu is easier for Python-related stuff)
 - Choose instance type (e.g., t2.micro for free tier)
 - Allow port 22, 80, and 443 in the security group
 - Download the PEM key and keep it safe
   
2. Connect to the EC2 Instance
   ssh -i "your-key.pem" ubuntu@your-ec2-public-ip

3. Install Required Packages
    # Update packages
      sudo apt update && sudo apt upgrade -y
    
    # Install Python and dependencies
      sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx -y
    
    # Install PostgreSQL
      sudo apt install postgresql postgresql-contrib -y

4. Configure PostgreSQL
  # Switch to postgres user
    sudo -i -u postgres

  # Create database and user
    psql
    CREATE DATABASE expense_tracker;
    CREATE USER postgres WITH PASSWORD 'postgres123';
    GRANT ALL PRIVILEGES ON DATABASE expense_tracker TO postgres;
    \q
    exit
5. Environment Configuration
   # Create .env file
      nano .env
   Past:
      DATABASE_URL=postgresql+asyncpg://postgres:postgres123@localhost/expense_tracker
      SECRET_KEY=mQN4BpX7zr!vT%KwY3RlVqStUv2y_A-HaPnMdShJeCk
      ALGORITHM=HS256
      ACCESS_TOKEN_EXPIRE_MINUTES=30
   
6. Clone Your FastAPI App or Upload It
   Use git clone <your-repo-url>, or Use scp from local to EC2:
   scp -i your-key.pem -r ./your-fastapi-project ubuntu@your-ec2-ip:/home/ubuntu/

7. Create and Activate a Virtual Environment
   cd your-fastapi-project
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

8. Test with Uvicorn
   uvicorn app.main:app --host 0.0.0.0 --port 8000

9. Set Up a Systemd Service (Optional but Recommended)
   sudo nano /etc/systemd/system/fastapi.service
   Paste this:
      [Unit]
      Description=FastAPI app
      After=network.target
      
      [Service]
      User=ubuntu
      WorkingDirectory=/home/ubuntu/expense_tracker
      ExecStart=/home/ubuntu/expense_tracker/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
      Restart=always
      
      [Install]
      WantedBy=multi-user.target

   Enable and start:
     sudo systemctl daemon-reexec
     sudo systemctl enable fastapi
     sudo systemctl start fastapi

10. Use Nginx as a Reverse Proxy
   Edit Nginx config:
     sudo nano /etc/nginx/sites-available/fastapi
   Paste:
      server {
      listen 80;
      server_name your-ec2-ip;
  
      location / {
          proxy_pass http://127.0.0.1:8000;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
        }
      }
   Enable it:
     sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled
     sudo nginx -t
     sudo systemctl restart nginx

 11. Visit Your App
     Now visit http://your-ec2-ip and you should see your FastAPI app live!


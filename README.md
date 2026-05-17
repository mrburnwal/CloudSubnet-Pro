# CloudSubnet Pro ☁️

A modern, fast, and responsive web application designed for DevOps engineers, Cloud Architects, and network administrators to calculate IP ranges, validate subnets, and plan AWS VPC architectures.

## 🚀 Features

- **CIDR Calculator**: Detailed breakdown of IP ranges, broadcasting, and usable IPs (including AWS-specific reserved IP calculations).
- **Subnet Splitter**: Divide large parent networks into smaller subnets based on a target mask or the number of required subnets.
- **AWS VPC Planner**: Automatically design multi-AZ architectures with recommended public, private, and database subnet allocations.
- **Overlap Validator**: Detect and highlight conflicts between multiple CIDR blocks.
- **Terraform Generator**: Export your planned VPC and subnets into clean, ready-to-use Terraform HCL code.
- **Visual Network Diagram**: A pure JS/CSS diagram visualizing your VPC architecture.

## 🛠️ Tech Stack

- **Frontend**: HTML5, Vanilla JavaScript, CSS3 (No frameworks, pure performance).
- **Backend**: Python (Flask) with the native `ipaddress` module for precise logic.
- **Design**: Glassmorphism aesthetic, full Dark/Light mode support, modern UI/UX.

## 💻 Getting Started (Local Development)

You can run this application locally using the built-in Flask backend:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mrburnwal/CloudSubnet-Pro.git
   cd CloudSubnet-Pro
   ```

2. **Set up a virtual environment (Optional but recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server:**

   ```bash
   python3 app.py
   ```

   The app will be available at `http://localhost:5001`.

## 🌐 Deployment (Static / GitHub Pages)

This application has been engineered to support a **100% serverless frontend mode**. The heavy subnet calculations have been ported to Vanilla JavaScript (`static/js/api.js`), allowing the app to run perfectly on static hosting providers like GitHub Pages without needing a Python backend.

Because this application could not deployed in Github Pages with full functionality as Github pages does not support python backend. I have deployed this application in Render.
Check it here: <https://cloudsubnet-pro.onrender.com/>

---
*Built with ❤️ for Network and Cloud Engineers.*

// State
let currentVPCPlan = null;

// Theme Toggle
function toggleTheme() {
    const html = document.documentElement;
    const icon = document.getElementById('theme-icon');
    if (html.getAttribute('data-theme') === 'dark') {
        html.setAttribute('data-theme', 'light');
        icon.className = 'fas fa-sun';
    } else {
        html.setAttribute('data-theme', 'dark');
        icon.className = 'fas fa-moon';
    }
}

// Navigation
function showSection(sectionId) {
    document.querySelectorAll('section').forEach(s => s.classList.remove('active'));
    document.getElementById(sectionId).classList.add('active');
    
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    const activeLink = Array.from(document.querySelectorAll('.nav-link')).find(l => l.getAttribute('onclick').includes(sectionId));
    if (activeLink) activeLink.classList.add('active');

    const titles = {
        'dashboard': 'Dashboard',
        'cidr-calc': 'CIDR Calculator',
        'splitter': 'Subnet Splitter',
        'planner': 'AWS VPC Planner',
        'overlap': 'Overlap Validator',
        'terraform': 'Terraform Generator'
    };
    document.getElementById('page-title').innerText = titles[sectionId] || 'CloudSubnet Pro';
}

// CIDR Calculator
async function calculateCIDR() {
    const cidr = document.getElementById('cidr-input').value;
    if (!cidr) return;
    
    const result = await API.calculateCIDR(cidr);
    const container = document.getElementById('cidr-results');
    const tbody = document.getElementById('cidr-table-body');
    
    tbody.innerHTML = `
        <tr><td>Network Address</td><td>${result.network_address}</td></tr>
        <tr><td>Broadcast Address</td><td>${result.broadcast_address}</td></tr>
        <tr><td>Total IPs</td><td>${result.total_ips}</td></tr>
        <tr><td>Usable IPs (Traditional)</td><td>${result.traditional_usable}</td></tr>
        <tr><td>AWS Usable IPs</td><td><span class="badge">${result.aws_usable}</span> (5 reserved)</td></tr>
        <tr><td>Subnet Mask</td><td>${result.subnet_mask}</td></tr>
        <tr><td>Wildcard Mask</td><td>${result.wildcard_mask}</td></tr>
        <tr><td>First Usable IP</td><td>${result.first_usable}</td></tr>
        <tr><td>Last Usable IP</td><td>${result.last_usable}</td></tr>
    `;
    
    container.style.display = 'block';
}

// Subnet Splitter
async function splitSubnet() {
    const parent = document.getElementById('split-parent').value;
    const mask = document.getElementById('split-mask').value;
    const count = document.getElementById('split-count').value;
    
    const results = await API.splitSubnet(parent, mask || null, count || null);
    const container = document.getElementById('split-results');
    
    container.innerHTML = '<h4>Generated Subnets:</h4>';
    const list = document.createElement('div');
    list.style.marginTop = '1rem';
    results.forEach(s => {
        list.innerHTML += `<div class="card" style="padding: 0.75rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
            <code>${s}</code>
            <button class="btn btn-secondary copy-btn" onclick="copyValue('${s}')">Copy</button>
        </div>`;
    });
    container.appendChild(list);
}

// AWS Planner
async function planVPC() {
    const parent = document.getElementById('vpc-cidr').value;
    const azs = document.getElementById('vpc-azs').value;
    const pub = document.getElementById('vpc-public').value;
    const priv = document.getElementById('vpc-private').value;
    const db = document.getElementById('vpc-db').value;

    const result = await API.planAWS(parent, azs, pub, priv, db);
    currentVPCPlan = { ...result, parent_cidr: parent };
    
    document.getElementById('planner-results').style.display = 'block';
    
    // Details
    const details = document.getElementById('plan-details');
    details.innerHTML = `
        <div class="grid">
            <div><h4 style="color: var(--success)">Public Subnets</h4>${result.public.map(s => `<div>${s}</div>`).join('')}</div>
            <div><h4 style="color: var(--accent-secondary)">Private Subnets</h4>${result.private.map(s => `<div>${s}</div>`).join('')}</div>
            <div><h4 style="color: var(--danger)">Database Subnets</h4>${result.database.map(s => `<div>${s}</div>`).join('')}</div>
        </div>
    `;

    // Diagram
    renderDiagram(result);

    // Recommendations
    const recs = document.getElementById('recommendations-list');
    recs.innerHTML = result.recommendations.map(r => `<li>${r}</li>`).join('');
}

// Overlap Validator
async function validateOverlap() {
    const input = document.getElementById('overlap-input').value;
    const cidrs = input.split('\n').filter(c => c.trim() !== '');
    
    const result = await API.validateOverlap(cidrs);
    const container = document.getElementById('overlap-results');
    
    if (result.has_overlap) {
        container.innerHTML = `<div class="card" style="border-color: var(--danger)">
            <h4 style="color: var(--danger)"><i class="fas fa-exclamation-circle"></i> Overlaps Detected!</h4>
            <ul style="margin-top: 1rem; color: var(--text-secondary)">
                ${result.overlaps.map(o => `<li>${o.message}</li>`).join('')}
            </ul>
        </div>`;
    } else {
        container.innerHTML = `<div class="card" style="border-color: var(--success)">
            <h4 style="color: var(--success)"><i class="fas fa-check-circle"></i> No overlaps found.</h4>
            <p>All CIDR blocks are unique and non-overlapping.</p>
        </div>`;
    }
}

// Terraform
async function generateTF() {
    if (!currentVPCPlan) {
        alert("Please generate a VPC plan first in the AWS Planner section.");
        showSection('planner');
        return;
    }

    const vpcConfig = {
        parent_cidr: currentVPCPlan.parent_cidr,
        public_subnets: currentVPCPlan.public,
        private_subnets: currentVPCPlan.private,
        database_subnets: currentVPCPlan.database
    };

    const result = await API.generateTF(vpcConfig);
    document.getElementById('tf-results').style.display = 'block';
    document.getElementById('tf-code').textContent = result.terraform;
}

// Utils
function copyValue(val) {
    navigator.clipboard.writeText(val);
    alert('Copied: ' + val);
}

function copyToClipboard(elementId) {
    const text = document.getElementById(elementId).textContent;
    navigator.clipboard.writeText(text);
    alert('Terraform code copied to clipboard!');
}

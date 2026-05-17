function renderDiagram(plan) {
    const container = document.getElementById('diagram-mount');
    container.innerHTML = '';

    // Internet Node
    const internet = createNode('Internet', 'fas fa-globe');
    container.appendChild(internet);
    container.appendChild(createArrow());

    // IGW Node
    const igw = createNode('Internet Gateway', 'fas fa-door-open');
    container.appendChild(igw);
    container.appendChild(createArrow());

    // Public Subnets
    if (plan.public && plan.public.length > 0) {
        const group = document.createElement('div');
        group.className = 'subnet-group';
        plan.public.forEach(cidr => {
            group.appendChild(createNode(`Public: ${cidr}`, 'fas fa-unlock', 'var(--success)'));
        });
        container.appendChild(group);
        container.appendChild(createArrow());
    }

    // Private Subnets
    if (plan.private && plan.private.length > 0) {
        const group = document.createElement('div');
        group.className = 'subnet-group';
        plan.private.forEach(cidr => {
            group.appendChild(createNode(`Private: ${cidr}`, 'fas fa-lock', 'var(--accent-secondary)'));
        });
        container.appendChild(group);
        container.appendChild(createArrow());
    }

    // DB Subnets
    if (plan.database && plan.database.length > 0) {
        const group = document.createElement('div');
        group.className = 'subnet-group';
        plan.database.forEach(cidr => {
            group.appendChild(createNode(`DB: ${cidr}`, 'fas fa-database', 'var(--danger)'));
        });
        container.appendChild(group);
    }
}

function createNode(text, iconClass, color) {
    const node = document.createElement('div');
    node.className = 'diagram-node animate-fade';
    if (color) node.style.borderColor = color;
    node.innerHTML = `<i class="${iconClass}" style="margin-right: 10px;"></i> ${text}`;
    return node;
}

function createArrow() {
    const arrow = document.createElement('div');
    arrow.className = 'diagram-arrow';
    return arrow;
}

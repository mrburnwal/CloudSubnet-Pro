const API = {
    async post(endpoint, data) {
        try {
            const response = await fetch(`/api${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'API Error');
            return result;
        } catch (error) {
            alert(error.message);
            throw error;
        }
    },

    calculateCIDR(cidr) {
        return this.post('/calculate-cidr', { cidr });
    },

    splitSubnet(parent, child_mask, num_subnets) {
        return this.post('/split-subnet', { parent, child_mask, num_subnets });
    },

    validateOverlap(cidrs) {
        return this.post('/validate-overlap', { cidrs });
    },

    planAWS(parent_cidr, azs, public, private, database) {
        return this.post('/aws-planner', { parent_cidr, azs, public, private, database });
    },

    generateTF(vpc_config) {
        return this.post('/generate-terraform', { vpc_config });
    }
};

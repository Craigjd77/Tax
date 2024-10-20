function calculateNetWorth() {
    const form = document.getElementById('financial-summary-form');
    const formData = new FormData(form);
    
    const realEstate = parseFloat(formData.get('real_estate')) || 0;
    const investments = parseFloat(formData.get('investments')) || 0;
    const cash = parseFloat(formData.get('cash')) || 0;
    
    const netWorth = realEstate + investments + cash;
    
    // Update net worth summary
    document.getElementById('display-name').textContent = formData.get('name');
    document.getElementById('display-net-worth').textContent = '$' + netWorth.toLocaleString();
    document.getElementById('net-worth-summary').style.display = 'block';
    
    // Update user inputs
    document.getElementById('update_age').value = formData.get('age');
    document.getElementById('update_salary').value = formData.get('salary');
    document.getElementById('current_net_worth').value = netWorth;
    document.getElementById('retirement_age').value = parseInt(formData.get('age')) + 20;
    document.getElementById('target_net_worth').value = Math.round(netWorth * 2);
}

document.getElementById('finance-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    
    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        updateResults(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

function updateResults(result) {
    document.getElementById('years-to-retirement').textContent = result.retirement_projection.years_to_retirement;
    document.getElementById('current-net-worth-display').textContent = '$' + result.retirement_projection.current_net_worth.toLocaleString();
    document.getElementById('target-net-worth-display').textContent = '$' + result.retirement_projection.target_net_worth.toLocaleString();
    document.getElementById('required-growth-rate').textContent = (result.retirement_projection.annual_growth_needed * 100).toFixed(2) + '%';
    document.getElementById('monthly-savings-needed').textContent = '$' + result.retirement_projection.monthly_savings_needed.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});

    updateRetirementChart(result.retirement_projection);
    updateTaxStrategies(result.tax_strategies);
    createAssetAllocationChart(result.assets);
}

function updateRetirementChart(projectionData) {
    const ctx = document.getElementById('retirement-chart').getContext('2d');
    const years = Array.from({length: projectionData.years_to_retirement}, (_, i) => i + 1);
    const projectedWealth = years.map(year => 
        projectionData.current_net_worth * Math.pow(1 + projectionData.annual_growth_needed, year)
    );

    if (window.retirementChart) {
        window.retirementChart.destroy();
    }

    window.retirementChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: years,
            datasets: [{
                label: 'Projected Wealth',
                data: projectedWealth,
                borderColor: '#3498db',
                fill: false
            }, {
                label: 'Target Wealth',
                data: Array(projectionData.years_to_retirement).fill(projectionData.target_net_worth),
                borderColor: '#2ecc71',
                borderDash: [5, 5],
                fill: false
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Retirement Wealth Projection'
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Years'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Wealth ($)'
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

function updateTaxStrategies(strategies) {
    const strategiesList = document.getElementById('strategies-list');
    strategiesList.innerHTML = '';
    strategies.forEach((strategy, index) => {
        const strategyElement = document.createElement('div');
        strategyElement.className = 'strategy-impact';
        strategyElement.innerHTML = `
            <span>${index + 1}. ${strategy.description}</span>
            <div class="impact-bar" style="width: ${strategy.impact}%;"></div>
        `;
        strategiesList.appendChild(strategyElement);
    });
}

function createAssetAllocationChart(assetData) {
    const ctx = document.getElementById('asset-chart').getContext('2d');
    
    const labels = Object.keys(assetData);
    const data = Object.values(assetData);
    
    if (window.assetChart) {
        window.assetChart.destroy();
    }
    
    window.assetChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    '#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6',
                    '#1abc9c', '#34495e', '#16a085', '#27ae60', '#2980b9'
                ]
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Asset Allocation'
            }
        }
    });
}

// Initialize charts with empty data
updateRetirementChart({
    years_to_retirement: 0,
    current_net_worth: 0,
    target_net_worth: 0,
    annual_growth_needed: 0
});
updateTaxStrategies([]);
createAssetAllocationChart({});
function parseCsvNumber(csvNumber) {
    return parseFloat(csvNumber.replace(',', '.'));
}

function buildBurndownData(csvData) {
    let total = 0;
    let data = [];

    csvData.splice(0, 1);
    csvData.sort((a, b) => a[0].localeCompare(b[0])).forEach(d => {
        total += parseCsvNumber(d[2]);
        data.push({
            x: d[0],
            y: total,
            amount: d[2],
            subject: d[1]
        });
    });

    return data;
}

function buildBurndownChart(csvData) {
    const ctx = document.getElementById('barChart').getContext('2d');

    const bdData = buildBurndownData(csvData);
    console.log(bdData);

    const data = {
        datasets: [
            {
                data: bdData,
                backgroundColor: function(context) {
                    return context.parsed.y < 0 ? 'red' : 'green';
                }
            }
        ]
    };

    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return context.raw.subject + ' ' + context.raw.amount + ' €';
                        }
                    }
                }
            }
        },
    });
}

function initCharts(options) {
    var csv_path = options.csv_path || "";
    var csv_options = options.csv_options || {};

    $.when($.get(csv_path)).then(
        function (data) {
            var csvData = $.csv.toArrays(data, csv_options);
            buildBurndownChart(csvData);
        }
    );

}


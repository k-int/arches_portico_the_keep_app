define([
    'knockout',
    'arches',
    'js-cookie',
    'templates/views/components/plugins/keep_integration_dashboard.htm'
], function (ko, arches, Cookies, KeepIntegrationDashboardTemplate) {

    const KeepIntegrationDashboardViewModel = function () {
        const self = this;

        this.selectedStartDate = ko.observable();
        this.selectedEndDate = ko.observable();

        this.errorMsg = ko.observable()

        this.onSubmit = function () {

            const startDate = new Date(self.selectedStartDate());
                const endDate = new Date(self.selectedEndDate());

                if (endDate < startDate) {
                    throw new Error("End date cannot be earlier than the start date.");
                }

                const formattedStartDate = `${startDate.getDate()}-${startDate.getMonth() + 1}-${startDate.getFullYear()}`
                const formattedEndDate = `${endDate.getDate()}-${endDate.getMonth() + 1}-${endDate.getFullYear()}`

                const url = `${window.location["origin"]}/resource/changes?from=${formattedStartDate}T00:00:00Z&to=${formattedEndDate}T00:00:00Z&sortField=id&sortOrder=asc&perPage=1000000&page=1`;
                
                fetch(url)
                    .then(response => response.json())
                    .then(({results}) => {
                        const resource_ids = results
                            .filter(resource => resource.tiles)
                            .map(resource => resource.resourceinstanceid)
                        return resource_ids
                })
                    .then(results => {

                        const start_month = startDate.toLocaleString('en-GB', {month: 'long'})
                        const end_month = endDate.toLocaleString('en-GB', {month: 'long'})
                        const start_day = String(startDate.getDate()).padStart(2, '0')
                        const end_day = String(endDate.getDate()).padStart(2, '0')
                        const period_string = `Mon_Export_${start_month}_${start_day}_to_${end_month}_${end_day}.xsd`

                        const body_object = JSON.stringify({
                            resourceid_list: results,
                            period_string: period_string
                        })

                        return fetch('/keep/export/', {
                                method: 'POST',
                                body: body_object,
                                headers: {
                                    "X-CSRFToken": Cookies.get('csrftoken'),
                                    'Content-Type': 'application/json',
                                }
                        })
                    .then(response => response.text())
                    .then(xmlString => {
                        console.log("xmlString", xmlString)
                        const blob = new Blob([xmlString], { type: 'application/xml' });
                        const blobUrl = URL.createObjectURL(blob);
                        window.open(blobUrl, '_blank');
                        setTimeout(() => URL.revokeObjectURL(blobUrl), 1000);
                    })
                    })
                    .catch(err => {
                        console.error("Fetch error", err)
                        self.errorMsg(err.message);
                    })
            return false
        };
    }

    return ko.components.register('keep_integration_dashboard', {
        viewModel: KeepIntegrationDashboardViewModel,
        template: KeepIntegrationDashboardTemplate
    });
});
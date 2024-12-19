define([
    'knockout',
    'arches',
    'templates/views/components/plugins/ciim_integration_dashboard.htm'
], function (ko, arches, CIIMIntegrationDashboardTemplate) {

    const CIIMIntegrationDashboardViewModel = function () {
        const self = this;

        this.selectedStartDate = ko.observable();
        this.selectedEndDate = ko.observable();

        this.errorMsg = ko.observable()

        this.onSubmit = function () {
            try {
                const startDate = new Date(self.selectedStartDate());
                const endDate = new Date(self.selectedEndDate());

                if (endDate < startDate) {
                    throw new Error("End date cannot be earlier than the start date.");
                }

                const formattedStartDate = `${startDate.getDate()}-${startDate.getMonth() + 1}-${startDate.getFullYear()}`
                const formattedEndDate = `${endDate.getDate()}-${endDate.getMonth() + 1}-${endDate.getFullYear()}`

                const url = `http://127.0.0.1:8000/resource/changes?from=${formattedStartDate}T00:00:00Z&to=${formattedEndDate}T00:00:00Z&sortField=id&sortOrder=asc&perPage=10&page=10`;

                fetch(url)
                    .then(response => response.json())
                    .then(({ results }) => {
                        console.log(results.map(resource => resource.resourceinstanceid))
                        self.errorMsg("");
                    })
                    .catch(err => {
                        console.error(err)
                        self.errorMsg(err.message);
                    })

            } catch (err) {
                console.error(err)
                self.errorMsg(err.message);
            }
            return false
        };
    }

    return ko.components.register('ciim_integration_dashboard', {
        viewModel: CIIMIntegrationDashboardViewModel,
        template: CIIMIntegrationDashboardTemplate
    });
});
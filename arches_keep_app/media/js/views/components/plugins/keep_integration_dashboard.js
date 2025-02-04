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

            self.errorMsg("")

            const startDate = new Date(self.selectedStartDate());
            const endDate = new Date(self.selectedEndDate());

            const start_month = startDate.toLocaleString('en-GB', {month: 'long'})
            const end_month = endDate.toLocaleString('en-GB', {month: 'long'})
            const start_day = String(startDate.getDate()).padStart(2, '0')
            const end_day = String(endDate.getDate()).padStart(2, '0')
            const period_string = `Mon_Export_${start_month}_${start_day}_to_${end_month}_${end_day}.xsd`

            if (endDate < startDate) {
                self.errorMsg("End date cannot be earlier than the start date.")
                throw new Error("End date cannot be earlier than the start date.");
            }

            const formattedStartDate = `${startDate.getDate()}-${startDate.getMonth() + 1}-${startDate.getFullYear()}`
            const formattedEndDate = `${endDate.getDate()}-${endDate.getMonth() + 1}-${endDate.getFullYear()}`

            const baseUrl = `${window.location["origin"]}/resource/changes?from=${formattedStartDate}T00:00:00Z&to=${formattedEndDate}T00:00:00Z&sortField=id&sortOrder=asc&perPage=100&page=`;
            
            fetch(baseUrl + "1")
                .then(response => response.json())
                .then((json) => {
                    const firstResults = 
                        json.results
                            .filter(resource => resource.tiles)
                            .map(resource => resource.resourceinstanceid)

                    const numberOfPages = json.metadata.numberOfPages
                    const fetchPromises = [firstResults]

                    for (let i = 2; i <= numberOfPages; i++) {
                        pageUrl = baseUrl + String(i)
                        fetchPromises.push(fetch(pageUrl)
                            .then(response => response.json())
                            .then(json => {
                                return json.results
                                    .filter(resource => resource.tiles)
                                    .map(resource => resource.resourceinstanceid)
                            })
                        )
                    }
                    return Promise.all(fetchPromises)
                })
                .then((results) => {
                    resourceid_list = [...results.flat()]

                    const body_object = JSON.stringify({
                        resourceid_list: resourceid_list,
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
                    const blob = new Blob([xmlString], { type: 'application/xml' });
                    const blobUrl = URL.createObjectURL(blob);

                    const a = document.createElement('a');
                    a.href = blobUrl;
                    a.download = 'keep_xml_export.xml';
                    document.body.appendChild(a);

                    a.click();
                    document.body.removeChild(a);

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
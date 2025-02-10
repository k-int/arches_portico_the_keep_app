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
        this.loading = ko.observable(false)
        this.loadingInfo = ko.observableArray()

        this.onSubmit = function () {

            try{
                const t0 = performance.now();
                
                self.loading(true)
                self.loadingInfo.removeAll()
                self.loadingInfo.push("Making initial API call...")
                self.errorMsg("")

                const startDate = new Date(self.selectedStartDate());
                const endDate = new Date(self.selectedEndDate());

                const start_month = startDate.toLocaleString('en-GB', {month: 'long'})
                const end_month = endDate.toLocaleString('en-GB', {month: 'long'})
                const start_day = String(startDate.getDate()).padStart(2, '0')
                const end_day = String(endDate.getDate()).padStart(2, '0')
                const period_string = `Mon_Export_${start_month}_${start_day}_to_${end_month}_${end_day}`

                if (endDate < startDate) {
                    self.loadingInfo.removeAll()
                    self.errorMsg("End date cannot be earlier than the start date.")
                    throw new Error("End date cannot be earlier than the start date.")
                }

                const formattedStartDate = `${startDate.getDate()}-${startDate.getMonth() + 1}-${startDate.getFullYear()}`
                const formattedEndDate = `${endDate.getDate()}-${endDate.getMonth() + 1}-${endDate.getFullYear()}`

                const baseUrl = `${window.location["origin"]}/resource/changes?from=${formattedStartDate}T00:00:00Z&to=${formattedEndDate}T00:00:00Z&sortField=id&sortOrder=asc&perPage=100&page=`;
                
                fetch(baseUrl + "1")
                    .then(response => response.json())
                    .then((json) => {

                        console.log("Number of resources: ", json.metadata.totalNumberOfResources) 
                        
                        const firstResults = json.results
                            .filter(resource => resource.tiles)
                            .map(resource => resource.resourceinstanceid)
                        
                        const numberOfPages = json.metadata.numberOfPages
                        const fetchPromises = [Promise.resolve(firstResults)]

                        self.loadingInfo.push(`${numberOfPages} pages to fetch...`)
                        self.loadingInfo.push(`Page 1 of ${numberOfPages} received...`)

                        let pageCounter = 2

                        for (let i = 2; i <= numberOfPages; i++) {
                            const pageUrl = baseUrl + String(i)
                            fetchPromises.push(
                                fetch(pageUrl)
                                .then(response => response.json())
                                .then(json => {
                                        let page = pageCounter++
                                        self.loadingInfo.pop()
                                        self.loadingInfo.push(`Page ${page} of ${numberOfPages} received...`)
                                        return json.results
                                            .filter(resource => resource.tiles)
                                            .map(resource => resource.resourceinstanceid)
                                    })
                            )
                        }
                        return Promise.all(fetchPromises)
                    })
                    .then((results) => {
                        const resourceid_list = [...results.flat()]

                        console.log("Number of resources filtered: ", resourceid_list.length) 

                        const t1 = performance.now();
                        console.log("Api calls complete. Time elapsed: ", t1-t0)
                        self.loadingInfo.push(`Converting results to XML...`)

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
                            self.loadingInfo.push(`Creating XML download...`)
                            const blob = new Blob([xmlString], { type: 'application/xml' });
                            const blobUrl = URL.createObjectURL(blob);

                            const a = document.createElement('a');
                            a.href = blobUrl;
                            a.download = period_string + '.xml';
                            document.body.appendChild(a);

                            a.click();
                            document.body.removeChild(a);

                            window.open(blobUrl, '_blank');
                            setTimeout(() => URL.revokeObjectURL(blobUrl), 1000);
                        })
                    })
                    .catch(err => {
                        self.loadingInfo.removeAll()
                        console.error("Fetch error", err)
                        self.errorMsg(err.message);
                    })
                    .finally (() => {
                        self.loading(false)
                        const t2 = performance.now();
                        console.log("XML compiled. Time elapsed: ", t2-t0)
                    })
            } catch (err) {
                console.error("Error", err)
                self.loading(false)
            } 
            return false
        };
    }

    return ko.components.register('keep_integration_dashboard', {
        viewModel: KeepIntegrationDashboardViewModel,
        template: KeepIntegrationDashboardTemplate
    });
});
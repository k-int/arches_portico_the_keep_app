define([
    'knockout',
    'arches',
    'templates/views/components/plugins/ciim_integration_dashboard.htm'
], function(ko, arches, CIIMIntegrationDashboardTemplate) {

    const CIIMIntegrationDashboardViewModel = function() {
        const self = this;

    };

    return ko.components.register('ciim_integration_dashboard', {
        viewModel: CIIMIntegrationDashboardViewModel,
        template: CIIMIntegrationDashboardTemplate
    });
});
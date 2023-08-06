/* jshint strict: false, white: true */
/* global cw: false, Namespace: false, _: false, AJAX_BASE_URL: false,
   ajaxFuncArgs: false */

/** filter form, aka facets, javascript functions
 *
 *  :organization: Logilab
 *  :copyright: 2003-2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
 *  :contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
 */

cw.cubes.searchui = {
    onDocumentReady: function () {
        // disable relswitch facet when a facet is being activated
        $(cw).bind('facets-content-loading', cw.cubes.searchui.disableSwitchFacet);
        // reload relswitch facet once facets are loaded
        $(cw).bind('facets-content-loaded', cw.cubes.searchui.reloadSwitchFacet);
    },

    disableSwitchFacet: function () {
        $('#cwRelationSwitch').hide();
    },

    reloadSwitchFacet: function (evt, divid, rql, vid, extraparams) {
        var $facetDiv = $('#cwRelationSwitch').closest('.facet');
        $facetDiv.loadxhtml(AJAX_BASE_URL,
                            ajaxFuncArgs('reload_switchfacet',
                                         null,
                                         rql),
                            'GET', 'swap');
    },

    onSwitchFacetChange: function ($select) {
        var switchUrl = $select.val();
        if (switchUrl.length > 0) {
            window.location = switchUrl;
        }
    }
};

$(function() {
    cw.cubes.searchui.onDocumentReady();
});

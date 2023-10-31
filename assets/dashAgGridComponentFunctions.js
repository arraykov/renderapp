var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};

dagcomponentfuncs.StockLink = function (props) {
    function openPopup() {
        var url = 'https://www.cefconnect.com/Details/SummaryPrint.aspx?Ticker=' + props.value;
        
        // Modify the width and height values as needed
        var windowFeatures = "width=1000,height=800,scrollbars=yes,resizable=yes,status=yes";
        
        window.open(url, "_blank", windowFeatures);
    }
    
    return React.createElement('a',
    {
        href: '#',
        onClick: openPopup // set the onClick event to our openPopup function
    }, props.value)
}

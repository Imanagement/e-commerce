function update_shipping(e){
    
    // Shipping option selection
    var
    // Searching select tag in DOM
    shipping_selection = document.getElementById('shipping_option')
    //Detecting id of chosen option in our select
    shipping_index = shipping_selection.options.selectedIndex,
    //Taking chosen option    
    shipping_selected_option = shipping_selection.options[shipping_index].getAttribute('value')
    // Taking attribute 'value'

    // City selection
    var
    // Searching select tag in DOM
    city_selection = document.getElementById('cities'),
    // Detecting id of chosen option in our select
    city_index = city_selection.options.selectedIndex,
    // Taking chosen option
    city_selected_option = city_selection.options[city_index],
    // Taking shipping cost and time
    shipping_days = city_selected_option.getAttribute('data-days'),
    shipping_cost = city_selected_option.getAttribute('data-cost'),
    // Finding span tag where the shipping days and cost would be displayed to
    shipping_days_html = document.getElementById('shipping-days'),
    shipping_cost_html = document.getElementById('shipping_amount'),
    // Div wrapper for shipping days to manupulate with its display
    shipping_days_wrapper = document.getElementById('shipping-days-wrapper');

    // Checking if the received option is courier
    if(shipping_selected_option === 'courier') {

        // Checking if recived data is not empty
        if(shipping_days >= 0 && shipping_cost >= 0) {
            
            // Filling data in HTML 
            shipping_days_html.textContent = String(shipping_days)
            shipping_cost_html.textContent = String(shipping_cost)

            if (shipping_days_wrapper.style.display === 'none') {
                shipping_days_wrapper.style.display = 'block';
            } else {
                return
            }
        
        // Checking if the received option is pickup
        }
    } else if(shipping_selected_option === 'pickup') {
            
        // Hiding the div with shipping time, and annuling shipping cost
        shipping_cost_html.textContent = String(0);
        shipping_days_wrapper.style.display = 'none';
        } else {
            return null;
        }
    
}
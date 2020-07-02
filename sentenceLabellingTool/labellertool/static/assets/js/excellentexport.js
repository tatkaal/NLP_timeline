(function ($){
    $(document).ready(function () {
        $('table').each(function () {
            var $table = $(this);

            var $button = $("<button type='button'>");
            $button.text("Export to csv");
            $button.insertAfter($table);

            $button.click(function () {
                // if($table.find('select').length){
                //     console.log($table.find('option:selected').text(), 'FOUND');
                // }else{
                //     console.log('NOOOOOOO')
                // // console.log(_quote_text(_trim_text($(this).text())), 'NOOOOOOOOOOOO');
                // }

                $table.table2csv({
                    file_name:  'test.csv',
                    // delivery: 'value'
                    header_body_space:  0
                });
                // window.location.href = 'data:text/csv;charset=UTF-8,' 
                // + encodeURIComponent(csv);
            });
        });
    })
})(jQuery);




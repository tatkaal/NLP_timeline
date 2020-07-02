(function ($) {
    const _trim_text = (text) => {
        return text.trim();
    };
    const _quote_text = (text) => {
        return '"' + text + '"';
    };
    const _export = (lines, file_name) => {
        const uri = 'data:text/csv;charset=utf-8,' + encodeURIComponent(lines.join('\n'));
        const el_a = document.createElement('a');
        el_a.href = uri;
        el_a.download = file_name;
        document.body.appendChild(el_a);
        el_a.click();
        document.body.removeChild(el_a);
    };



    const init = (tb, options) => {
        let lines = [];
        $(tb).find('thead>tr').each(function () {
            let line = [];
            $(this).find('th').each(function () {
                line.push(_quote_text(_trim_text($(this).text())));
            });
            lines.push(line.splice(0).toString());
        })
        
        
        
        for (let i = 0; i < options.header_body_space; i++) lines.push('\n');
        $(tb).find('tbody>tr').each(function () {
            let line = [];
            $(this).find('td').each(function () {
               
              /* If <td> has <select>, CSV have selected value */
            //   console.log($(this).find('option:selected').text());
              
              if($(this).find('select').length > 0){
                var optVal = $(this).find('select').val();
                // var selectVal = $(this).find('option[value="'+optVal+'"]').text();
                var selectVal = $(this).find('option:selected').text()
                line.push(_quote_text(_trim_text(selectVal)));
                
              }
              else{
                line.push(_quote_text(_trim_text($(this).text())));
              }
                
                   
                
            });
            lines.push(line.splice(0).toString());
        })
        _export(lines, options.file_name)
    };



    $.fn.extend({
        table2csv: function (options) {
            const default_options = {
                file_name: 'table_records.csv',
                header_body_space: 1
            };
            options = $.extend(default_options, options);
            init(this, options);
        }
    })
})(jQuery);
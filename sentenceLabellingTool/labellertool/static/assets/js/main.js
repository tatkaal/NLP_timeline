function add_cat(e, category='', index='', sentences='', pos=''){
    e.preventDefault();
    console.log(category, index, sentences, pos);
    $.ajax({
        type:'POST',
        url: 'save_csv',
        data:{
            'category':category,
            'index': index,
            'sentences': sentences,
            'pos':pos
        }
    });
}

var fileIndex = ''

$(document).ready(function() {

//   $("#btnSubmit").click(function(event) {
$("form#formFile").submit(function(e) {

    $("tbody tr").remove();  

    var form_data = new FormData($('#formFile')[0]);
    event.preventDefault();
    $.ajax({
        method:"POST",
        url:"/",
        // url:"{{ url_for('uploader') }}",
        data:form_data,
        processData: false,
        contentType: false,
        success:function(data){
            try {
                $('#formFile')[0].reset()
            } catch (error) {
                console.log(error)
            }
            // console.log(data)
            console.log('Working')
            // console.log(data['file_index'])
            console.log('--------------------')
            fileIndex = data['file_index'];
            // console.log(data['sentences']);
            showlines(data['sentences'], data['pos'])
        },
        error: function(xhr, ajaxOptions, thrownError){
            //if fails  
            console.log(xhr.responseText)   
        }
    });

    function setAttributes(el, attrs) {
        for(var key in attrs) {
          el.setAttribute(key, attrs[key]);
        }
    }

    

    function showlines(sentences, pos) {

        // $('#label').empty();
        if (sentences) {
            // var summary = document.createElement('h5');
            // summary.innerHTML = "<b>Labels</b>:<br />";
            // $('#label').append(summary);

            var tbl = document.getElementsByTagName('tbody')[0];
            
            // tbl.style.width = '100%';
            // tbl.setAttribute('border', '1');
            // var tbdy = document.createElement('tbody');
            var arr = []
            var category = ['Select','Name', 'Experience', 'Skills']
            var arr_sec = []
            for (var i = 0; i < (sentences.length); i++) {
                var tr = tbl.insertRow(i);
                var tryit;
                
                if(sentences[i].length > 5)
                {
                    tryit=sentences[i].length/2
                }
                else
                {
                    tryit=sentences[i].length
                }
                arr = [i+1, sentences[i].slice(0,tryit), pos[i].slice(0,pos[i].length)]
                // arr_sec = [0, pos[i].slice(0,pos[i].length)]
                for (var j=0; j<3;j++)
                {
                    var th = tr.insertCell(j);
                    // var th2 = tr.insertCell(j+1);
                    if (j==1){
                        // console.log(arr[j])
                        // var collapse = document.createElement('<div class="collapse">'+
                        //                 '<div class="card card-body">'+
                        //                 'Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident.'+
                        //                 '</div>'+
                        // '</div>')
                        var collapse = document.createElement('div');
                        setAttributes(collapse, {'class': 'collapse', 'id': 'collapseEx-'+i+''});
                        var card = document.createElement('div');
                        card.setAttribute('class', 'card card-body');
                        card.innerHTML = sentences[i];
                        collapse.appendChild(card);
                        var anchor = document.createElement('a')
                        setAttributes(anchor, {'data-toggle':"collapse", 'href':'#collapseEx-'+i+'', 'role':"button", 'aria-expanded':"false", 'aria-controls':'collapseEx-'+i+''})
                        anchor.innerHTML = arr[j];
                        th.appendChild(anchor)
                        th.appendChild(collapse);
                        // th.appendChild(document.createElement('<a type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal">'+arr[j].toString()+'</a>'));
                    }
                    else{
                        th.innerHTML = arr[j]
                    }
                }
                var th = tr.insertCell(3);
                var dropdown = '<div class="dropdown">'+
                // '<form action="" name="FILTER">'+
                    '<select name="filter_for class="dropdown-menu" id="dropdown-'+i+'"" >'+
                        
                    '</select>'+
                // '</form>'+
            '</div>'
                $(th).append(dropdown);


                for (var j=0;j<4;j++){
                    $('#dropdown-'+i+'').append('<option class="dropdown-item" onclick="add_cat(event, category=\''+category[j]+'\', '+i+', \''+sentences[i]+'\', \'' + pos[i]+'\')">'+category[j]+'</option><br>');
                }

                tbl.appendChild(tr);
              }
            // tbl.appendChild(tbdy);
            // $('#label').append(tbl);
            // body.appendChild(tbl)

            // for (var index in sentences) {
            //     var listElement = document.createElement('li');
            //     listElement.innerHTML = sentences[index];
            //     uList.appendChild(listElement);
            // }

            // $('#label').append(uList);
        }
        $('table').each(function () {
            var $table = $(this);
            $table.table2csv({
                //C:/Users/zerad/Desktop/dolphinlab-master/Dharmajit/summarize-webpage/
                file_name:  'test-'+fileIndex+'.csv',
                header_body_space:  0
            });
        });
        // } else {
        //     var label = document.createElement('p');
        //     label.innerHTML = "<b>Labels</b>: " + sentences;
        //      $('#label').append(summary);
        // }

        // $('#label').hide().fadeIn(1000);
    }

  })});

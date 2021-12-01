$('.select2').select2();

function dropdownlist(placeholder, dropdown, url)
{
    $(dropdown).select2({
        placeholder: placeholder,
        ajax: {
            url: url,
            dataType: 'json',
            delay: 250,
            data: function (data)
            {
                return {
                    searchTerm: data.term
                };
            },
            processResults: function (response)
            {
                return {
                    results: response
                };
            },
            cache: true
        }
    });
};

function hide_modal(params)
{
    setTimeout(function ()
    {
        $('#modal-default').modal('hide');
    }, 1000);
}

let arr_msgicons = ['', 'fal fa-save fa-lg', 'fas fa-pencil-alt fa-lg', 'fal fa-trash-alt fa-lg'];
function msgAlert(header, remarks, ico)
{
    $(document).Toasts('create', {
        class: 'bg-white',
        title: '<span style="font-size: 12px;"> ' + header + ' </span>',
        subtitle: '<a href="" class="nav-link" id="">reserved!</a>',
        position: 'bottomRight',
        icon: arr_msgicons[ico],
        body: '<div class="col-md-9 row" style="width: 300px"><span style="font-size:13px;">' + remarks + '</span></div>',
        autohide: true,
        delay: 10000,
    });
};
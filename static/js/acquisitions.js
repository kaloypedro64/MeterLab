window.onload = function ()
{

    loadAcquisition(0);
    loadAcquisition(1);

};

function loadAcquisition(params)
{
    var tbl = "acqTable";
    if (params == 1) tbl = "acqTable_mSeal";
    acqTable = $('#' + tbl + '').DataTable({
        "searching": true,
        "processing": true,
        "stateSave": true,
        "info": false,
        "paging": true,
        "lengthChange": true,
        "autoWidth": false,
        "responsive": true,
        "columnDefs": [
            { "targets": [0], "searchable": false, "orderable": false, "visible": true },
            // { "targets": [5], "className": "text-left" }
        ],
        "keys": true,
        "keys": { "blurable": false },
        "select": true,
        "select": {
            "style": 'multi',
            "selector": 'td:first-child',
        },
        "serverSide": true,
        "processing": true,
        "ajax": function (data, callback, settings)
        {
            var sort_column_name = data.columns[data.order[0].column].data.replace(/\./g, "__");
            var direction = "";
            if (data.order[0].dir == "desc") { direction = "-" };
            $.get(acqListUrl, {
                acqtype: params,
                limit: data.length,
                start: data.start,
                filter: data.search.value,
                order_by: direction + sort_column_name
            }, function (res)
            {
                callback({
                    recordsTotal: res.length,
                    recordsFiltered: res.length,
                    data: res.objects
                });
            });
        },
        columns: [
            {
                "data": "id", "render": function (data, type, row)
                {
                    return '<td class="selected"><input type="checkbox" id="item_20" value="20"><label for="item_20"><span></span></label></td>'
                }
            },
            {
                "data": "id", "render": function (data, type, row)
                {
                    // if ('{{ request.user.is_superuser }}' == 'True')
                    // {
                    if (row["status"] == 1)
                    {
                        return '<div class="btn-group">' +
                            '<a href="#" class="btn btn-warning btn-xs" title="Accept" onclick = "acquisition_response(' + row["id"] + ', 0)" ><i class="fal fa-check mr-1"></i><span style="font-size: 12px;">Accept</span></a>' +
                            '<a href="#" class="btn btn-danger btn-xs" title="Cancel" onclick="acquisition_response(' + row["id"] + ', 1)" ><i class="fal fa-times"></i><span style="font-size: 12px;"></span></a>' +
                            '</div>'
                        // '<span class="badge bg-success float-right" style="font-size:8px"> 3 </span>'

                    }
                    else
                    {
                        return '<div class="input-group-prepend">' +
                            '  <button type="button" class="btn btn-info btn-xs dropdown-toggle dropdown-icon mr-1" data-toggle="dropdown">Action </button>' +
                            '    <div class="dropdown-menu">' +
                            '      <a class="dropdown-item" href="#" onclick="modal_editacquisition(' + row["id"] + ')"><i class="fal fa-pencil-alt mr-1"></i> Edit</a>' +
                            '      <a class="dropdown-item" onclick="meter_delete(' + row["id"] + ')"><i class="fal fa-trash-alt mr-1"></i> Delete</a>' +
                            '    </div>' +
                            '  </div >'
                    }
                }
            },
            {
                "data": "transactiondate", "render": function (data, type, row)
                {
                    if (row["status"] == 1)
                    {
                        return '<td style="width: fit-content;"> ' + data + '</td>'

                    }
                    else
                    {
                        if (params == 0)
                            return '<td style="width: fit-content;"> <a href="acqadd/' + row["id"] + '" style="color:primary">' + data + '</a></td>'
                        else
                            return '<td style="width: fit-content;"> <a href="acqadds/' + row["id"] + '">' + data + '</a></td>'
                    }
                }
            },
            { "data": "rrnumber" },
            { "data": "supplierid__suppliername" },
            { "data": "supplierid__address" },
        ],
        // "dom": '<"top"i>rt<"bottom"flp><"clear">',
    });
    acqTable.column(0).visible(false);
}

function modal_acquisition(params)
{
    if (params != undefined)
    {
        $('#id_acqtype').val(1);
        $('#modal-acquisition').find('.modal-title').text("Meter Seal Acquisition");
    } else
    {
        $('#id_acqtype').val(0);
        $('#modal-acquisition').find('.modal-title').text("Meter Acquisition");
    }
    dropdownlist('Search RRNumbers', '.dropdown-list-rrnumber', urlrrnumbers);
    dropdownlist('Search Supplier', '.dropdown-list-suppliers', urlsuppliers);
    $('#modal-acquisition').modal('show').draggable({ handle: ".modal-header" });
    // select_supplier(0);
}

function modal_editacquisition(params)
{
    $.ajax({
        url: acqEdit.replace('0', params),
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        contentType: false,
        data: { id: params, },
        success: function (data)
        {
            if (data.msg == 'found')
            {
                $('#modal-editacquisition').modal('show').draggable({ handle: ".modal-header" });
            }
        },
        error: function (e)
        {
            alert('err: meter list 158');
        }
    });
}

function acquisition_save()
{
    var transactiondate = $('#id_transactiondate').val();
    var rrno = $('#id_rrnumber option:selected').html();
    var supplierid = $('#id_supplierid').val();
    var suppliername = $('#lblSupplierName').html();
    var address = $('#lblAddress').html();
    var csrf = document.querySelector('[name="csrfmiddlewaretoken"]').value;
    var acqtype = $('#id_acqtype').val();
    $.ajax({
        url: acqSave,
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        contentType: false,
        data: {
            csrfmiddlewaretoken: csrf,
            transactiondate: transactiondate,
            rrno: rrno,
            supplierid: supplierid,
            acqtype: acqtype,
            suppliername: suppliername,
            address: address
        },
        success: function (data)
        {
            if (data.msg == 'saved')
            {
                $('#modal-acquisition').hide();
                Swal.fire('Saved!', ' Successfully saved!', 'success');
                if (acqtype == 0)
                    window.open(acqAdd.replace('0', data.id), "_self");
                else
                    window.open(acqAdds.replace('0', data.id), "_self");
            }
        },
        error: function (e)
        {
            alert('err: acquisition_save');
        }
    });
}

function select_rrnumber(params)
{
    var id = $('#id_rrnumber').val();
    $.ajax({
        url: urlsrrnumbers,
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        contentType: false,
        data: { id: id, },
        success: function (data)
        {
            var suppliers = $('#id_supplier');
            var newOption = new Option(data.form[0][3], data.form[0][2], true, true);
            suppliers.append(newOption).trigger('change');
            $('#id_supplierid').val(data.form[0][2]);
        },
        error: function (e)
        {
            alert('err: selected_consumer');
        }
    });
}

function select_supplier(params)
{
    // var e = document.getElementById("id_supplier");
    // if (params == null) params = e.selectedIndex
    // var option = e.options[params];
    // // var attrs = option.attributes;
    // var data = option.getAttribute("data-address");
    // $('#id_supplierid').val(option.value);
    // document.getElementById('lblAddress').innerHTML = data;

    var id = $('#id_supplier').val();
    $.ajax({
        url: urlssuppliers,
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        contentType: false,
        data: { id: id, },
        success: function (data)
        {
            // var lastoption = new Option(data.form[0][2], true, true);
            // $('#id_supplier').append(lastoption);
            // $('#id_supplier').trigger('change');

            // id_supplier id_supplierid
            $('#lblSupplierName').html(data.form[0][1]);
            $('#lblAddress').html(data.form[0][2]);
        },
        error: function (e)
        {
            alert('err: selected_consumer');
        }
    });
}

function meter_delete(id)
{
    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        confirmButtonText: "Yes, delete it!",
        showCancelButton: true,
        cancelButtonColor: '#d33',
        icon: "question",
    }).then((result) =>
    {
        if (result.isConfirmed)
        {
            $.ajax({
            // url: acqDelete.replace('0', id),
            url: urlresponse,
            type: 'GET',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            contentType: false,
            data: { id: id, response:1 },
            success: function (data)
            {
                if (data.msg == 'canceled')
                {
                    Swal.fire('Deleted!', ' Successfully deleted!', 'success');
                    reload_dt();
                }
            },
            error: function (e)
            {
                alert('err: meter list 158');
            }
        });
        } else if (result.isDenied)
        {
            Swal.fire('Changes are not saved', '', 'info')
        }
    });
}

function acquisition_response(params, response)
{
    title_msg = "";
    buttom_txt = "";
    text_msg = "";
    ico = "question";
    if (response == 0)
    {
        title_msg = "Are you sure to accept this entry?";
        buttom_txt = "Yes, accept it!";
        ico = "question";
        text_msg = "";
    }
    else
    {
        title_msg = 'Are you sure?';
        buttom_txt = "Yes, cancel it!";
        ico = "warning";
        text_msg = "You won't be able to revert this!";
    }
    Swal.fire({
        title: title_msg,
        text: text_msg,
        // showDenyButton: true,
        confirmButtonText: buttom_txt,
        // confirmButtonColor: '#00cc00',
        showCancelButton: true,
        cancelButtonColor: '#d33',
        // denyButtonText: `Don't save`,
        icon: ico,
    }).then((result) =>
    {
        if (result.isConfirmed)
        {
            $.ajax({
                url: urlresponse,
                type: 'GET',
                dataType: 'json',
                contentType: 'application/json; charset=utf-8',
                contentType: false,
                data: { id: params, response: response },
                success: function (data)
                {
                    if (data.msg == 'accepted')
                    Swal.fire('Accepted!', ' Successfully accepted!', 'success');
                    else
                    Swal.fire('Canceled!', ' Successfully canceled!', 'danger');
                    reload_dt();
                },
                error: function (e)
                {
                    Swal.fire('Error!', e, 'danger');
                }
            });
        } else if (result.isDenied)
        {
            Swal.fire('Changes are not saved', '', 'info')
        }
    });


    function reload_dt()
    {
        $("#acqTable").dataTable().fnDestroy();
        loadAcquisition(0);
    }
    // var ok;
    // if (response == 0) ok = confirm('Are you sure to accept this entry?');
    // if (response == 1) ok = confirm('Are you sure to delete this entry?');
    // if (ok == true)
    // {
    //     $.ajax({
    //         url: urlresponse,
    //         type: 'GET',
    //         dataType: 'json',
    //         contentType: 'application/json; charset=utf-8',
    //         contentType: false,
    //         data: { id: params, response: response },
    //         success: function (data)
    //         {
    //             if (data.msg == 'accepted') Swal.fire('Accepted!', ' Successfully accepted!', 'success');
    //             if (data.msg == 'canceled') Swal.fire('Canceled!', ' Successfully canceled!', 'danger');
    //             $('#acqTable').DataTable.ajax.reload(null, false);

    //         },
    //         error: function (e)
    //         {
    //             Swal.fire('Error!', e, 'danger');
    //         }
    //     });
    // }
}

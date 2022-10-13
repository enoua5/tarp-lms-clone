var _base_template_load_functions = [];

function registerLoadFunction(func)
{
    _base_template_load_functions.push(func)
}

function _base_template_onload()
{
    for(let i of _base_template_load_functions)
        i();
}
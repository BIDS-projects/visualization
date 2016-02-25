from visualization import app
import os

if __name__ == '__main__':
    jinja_options = app.jinja_options.copy()
    jinja_options.update(dict(
    block_start_string='<%',
    block_end_string='%>',
    variable_start_string='%%',
    variable_end_string='%%',
    comment_start_string='<#',
    comment_end_string='#>',
    ))
    app.jinja_options = jinja_options
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

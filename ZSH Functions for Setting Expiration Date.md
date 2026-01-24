# ZSH Functions for Setting Expiration Date

→ Add these to your `.zshrc` file 

```bash
odoo-expire13() {
    local db=$1
    if [ -z "$db" ]; then
        echo "Usage: odoo-expire13 <database_name>"
        return 1
    fi
    
    local exp_date=$(date -v+2m +%Y-%m-%d)
    
    cd-odoo13 && \
    source .venv/bin/activate && \
    echo "env['ir.config_parameter'].sudo().set_param('database.expiration_date', '$exp_date'); env.cr.commit()" | \
    ./odoo-bin shell -d $db --addons-path=addons,enterprise --limit-memory-hard=0
}

odoo-expire14() {
    local db=$1
    if [ -z "$db" ]; then
        echo "Usage: odoo-expire14 <database_name>"
        return 1
    fi
    
    local exp_date=$(date -v+2m +%Y-%m-%d)
    
    cd-odoo14 && \
    source .venv/bin/activate && \
    echo "env['ir.config_parameter'].sudo().set_param('database.expiration_date', '$exp_date'); env.cr.commit()" | \
    ./odoo-bin shell -d $db --addons-path=addons,enterprise --limit-memory-hard=0
}

odoo-expire15() {
    local db=$1
    if [ -z "$db" ]; then
        echo "Usage: odoo-expire15 <database_name>"
        return 1
    fi
    
    local exp_date=$(date -v+2m +%Y-%m-%d)
    
    cd-odoo15 && \
    source .venv/bin/activate && \
    echo "env['ir.config_parameter'].sudo().set_param('database.expiration_date', '$exp_date'); env.cr.commit()" | \
    ./odoo-bin shell -d $db --addons-path=addons,enterprise --limit-memory-hard=0
}

odoo-expire16() {
    local db=$1
    if [ -z "$db" ]; then
        echo "Usage: odoo-expire16 <database_name>"
        return 1
    fi
    
    local exp_date=$(date -v+2m +%Y-%m-%d)
    
    cd-odoo16 && \
    source .venv/bin/activate && \
    echo "env['ir.config_parameter'].sudo().set_param('database.expiration_date', '$exp_date'); env.cr.commit()" | \
    ./odoo-bin shell -d $db --addons-path=addons,enterprise --limit-memory-hard=0
}

odoo-expire17() {
    local db=$1
    if [ -z "$db" ]; then
        echo "Usage: odoo-expire17 <database_name>"
        return 1
    fi
    
    local exp_date=$(date -v+2m +%Y-%m-%d)
    
    cd-odoo17 && \
    source .venv/bin/activate && \
    echo "env['ir.config_parameter'].sudo().set_param('database.expiration_date', '$exp_date'); env.cr.commit()" | \
    ./odoo-bin shell -d $db --addons-path=addons,enterprise --limit-memory-hard=0
}

odoo-expire18() {
    local db=$1
    if [ -z "$db" ]; then
        echo "Usage: odoo-expire18 <database_name>"
        return 1
    fi
    
    local exp_date=$(date -v+2m +%Y-%m-%d)
    
    cd-odoo18 && \
    source .venv/bin/activate && \
    echo "env['ir.config_parameter'].sudo().set_param('database.expiration_date', '$exp_date'); env.cr.commit()" | \
    ./odoo-bin shell -d $db --addons-path=addons,enterprise --limit-memory-hard=0
}

odoo-expire19() {
    local db=$1
    if [ -z "$db" ]; then
        echo "Usage: odoo-expire19 <database_name>"
        return 1
    fi
    
    local exp_date=$(date -v+2m +%Y-%m-%d)
    
    cd-odoo19 && \
    source .venv/bin/activate && \
    echo "env['ir.config_parameter'].sudo().set_param('database.expiration_date', '$exp_date'); env.cr.commit()" | \
    ./odoo-bin shell -d $db --addons-path=addons,enterprise --limit-memory-hard=0
}
```


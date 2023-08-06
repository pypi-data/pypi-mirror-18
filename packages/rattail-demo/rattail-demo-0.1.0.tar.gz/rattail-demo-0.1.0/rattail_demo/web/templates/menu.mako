## -*- coding: utf-8 -*-

<%def name="main_menu_items()">

    % if request.has_any_perm('products.list', 'vendors.list', 'brands.list', 'families.list', 'reportcodes.list'):
        <li>
          <a>Products</a>
          <ul>
            % if request.has_perm('products.list'):
                <li>${h.link_to("Products", url('products'))}</li>
            % endif
            % if request.has_perm('vendors.list'):
                <li>${h.link_to("Vendors", url('vendors'))}</li>
            % endif
            % if request.has_perm('brands.list'):
                <li>${h.link_to("Brands", url('brands'))}</li>
            % endif
            % if request.has_perm('families.list'):
                <li>${h.link_to("Families", url('families'))}</li>
            % endif
            % if request.has_perm('reportcodes.list'):
                <li>${h.link_to("Report Codes", url('reportcodes'))}</li>
            % endif
          </ul>
        </li>
    % endif

    % if request.has_any_perm('people.list', 'customers.list', 'employees.list'):
        <li>
          <a>People</a>
          <ul>
            % if request.has_perm('people.list'):
                <li>${h.link_to("All People", url('people'))}</li>
            % endif
            % if request.has_perm('customers.list'):
                <li>${h.link_to("Customers", url('customers'))}</li>
            % endif
            % if request.has_perm('employees.list'):
                <li>${h.link_to("Employees", url('employees'))}</li>
            % endif
          </ul>
        </li>
    % endif

    % if request.has_any_perm('stores.list', 'departments.list', 'subdepartments.list'):
        <li>
          <a>Company</a>
          <ul>
            % if request.has_perm('stores.list'):
                <li>${h.link_to("Stores", url('stores'))}</li>
            % endif
            % if request.has_perm('departments.list'):
                <li>${h.link_to("Departments", url('departments'))}</li>
            % endif
            % if request.has_perm('subdepartments.list'):
                <li>${h.link_to("Subdepartments", url('subdepartments'))}</li>
            % endif
          </ul>
        </li>
    % endif

    % if request.has_any_perm('batch.handheld.list', 'batch.inventory.list'):
        <li>
          <a>Batches</a>
          <ul>
            % if request.has_perm('batch.handheld.list'):
                <li>${h.link_to("Handheld", url('batch.handheld'))}</li>
            % endif
            % if request.has_perm('batch.inventory.list'):
                <li>${h.link_to("Inventory", url('batch.inventory'))}</li>
            % endif
          </ul>
        </li>
    % endif

    % if request.has_any_perm('users.list', 'roles.list', 'settings.list'):
        <li>
          <a>Admin</a>
          <ul>
            % if request.has_perm('users.list'):
                <li>${h.link_to("Users", url('users'))}</li>
            % endif
            % if request.has_perm('roles.list'):
                <li>${h.link_to("Roles", url('roles'))}</li>
            % endif
            % if request.has_perm('settings.list'):
                <li>${h.link_to("Settings", url('settings'))}</li>
            % endif
          </ul>
        </li>
    % endif

    % if request.user:
        <li>
          <a${' class="root-user"' if request.is_root else ''|n}>${request.user}${" ({})".format(inbox_count) if inbox_count else ''}</a>
          <ul>
            % if request.is_root:
                <li class="root-user">${h.link_to("Stop being root", url('stop_root'))}</li>
            % elif request.is_admin:
                <li class="root-user">${h.link_to("Become root", url('become_root'))}</li>
            % endif
            <li>${h.link_to("Change Password", url('change_password'))}</li>
            <li>${h.link_to("Logout", url('logout'))}</li>
          </ul>
        </li>
    % else:
        <li>${h.link_to("Login", url('login'))}</li>
    % endif

</%def>

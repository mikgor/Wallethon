import {Routes} from '@angular/router';
import {APP_ROUTES} from '../routes-config';
import {DashboardComponent} from './components/dashboard/dashboard.component';
import {AddEditStockTransactionComponent} from './components/transactions/add-edit-transaction/add-edit-stock-transaction.component';


export const MainRoutes: Routes = [
    { path: `${APP_ROUTES.dashboard}`, component: DashboardComponent },
    { path: `${APP_ROUTES.addTransaction}`,   component: AddEditStockTransactionComponent },
    { path: `${APP_ROUTES.editTransaction}/:id`,   component: AddEditStockTransactionComponent },
  ];

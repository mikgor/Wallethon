import { Component, OnInit } from '@angular/core';
import {BaseAddEditPageComponent} from '../../../../shared/components/base-add-edit-page/base-add-edit-page.component';
import {Router} from '@angular/router';
import {FormBuilder, Validators} from '@angular/forms';
import {StockTransaction} from '../../dashboard/models/StockTransaction';
import {StockTransactionsService} from '../../../../shared/services/stock-transactions.service';
import {DashboardService} from '../../dashboard/services/dashboard.service';
import {CompanyStock} from '../../dashboard/models/CompanyStock';
import {AutoCompleteFilter} from '../../../../shared/models/auto-complete-filter';
import {MoneyService} from '../../../../shared/services/money.service';
import {autoCompleteValidator} from '../../../../shared/validators/auto-complete-validator';
import {UserBroker} from '../../dashboard/models/UserBroker';
import {ApiResponseHandlingService} from '../../../../shared/services/api-response-handling.service';
import {APP_ROUTES} from '../../../../routes-config';

@Component({
  selector: 'app-add-edit-transaction',
  templateUrl: './add-edit-stock-transaction.component.html',
  styleUrls: ['./add-edit-stock-transaction.component.scss']
})
export class AddEditStockTransactionComponent extends BaseAddEditPageComponent implements OnInit {
  protected stockTransaction: StockTransaction;
  public companyStocks: CompanyStock[];
  public userBrokers: UserBroker[];
  public stockTransactionTypes;
  public stockAutoCompleteFilter: AutoCompleteFilter;
  public currenciesAutoCompleteFilter: AutoCompleteFilter;
  public loading = false;

  constructor(
    private formBuilder: FormBuilder,
    private router: Router,
    private stockTransactionsService: StockTransactionsService,
    private dashboardService: DashboardService,
    private moneyService: MoneyService,
    public apiResponseHandlingService: ApiResponseHandlingService,
    ) { super(apiResponseHandlingService); }

  ngOnInit(): void {
    this.stockTransactionTypes = this.stockTransactionsService.getStockTransactionTypes();
    this.stockAutoCompleteFilter = new AutoCompleteFilter('symbol', {1: '', 2: 'startswith'},
      this.dashboardService.getCompanyStocksWithFilters.bind(this.dashboardService));
    this.currenciesAutoCompleteFilter = new AutoCompleteFilter('symbol', {1: 'startswith'},
      this.moneyService.getCurrencies.bind(this.moneyService), true);
    this.dashboardService.getUserBrokers().subscribe(userBrokers => {
      this.userBrokers = userBrokers;
      if (userBrokers.length > 0) {
        this.controls.broker.setValue(userBrokers[0].id);
      }
    });
    this.initForm();
  }

  private initForm() {
    this.form = this.formBuilder.group(({
      type: ['BUY', Validators.required],
      companyStock: ['', [Validators.required, autoCompleteValidator(this.stockAutoCompleteFilter)]],
      stockQuantity: [1, Validators.min(0.00000001)],
      date: ['', Validators.required],
      perStockPrice: [0.01, Validators.min(0.01)],
      currency: ['USD', [Validators.required, autoCompleteValidator(this.currenciesAutoCompleteFilter)]],
      tax: [0.00, Validators.min(0.00)],
      commission: [0.00, Validators.min(0.00)],
      broker: ['', Validators.required],
    }));
  }


  onSubmit() {
    if (!this.isFormValid()) {
      return;
    }

    const currency = this.currenciesAutoCompleteFilter.getValue(this.controls.currency.value).symbol;
    this.stockTransaction = new StockTransaction(null,
      this.controls.type.value,
      this.stockAutoCompleteFilter.getValue(this.controls.companyStock.value),
      this.controls.date.value,
      this.controls.perStockPrice.value,
      currency,
      this.controls.stockQuantity.value,
      this.controls.tax.value,
      currency,
      this.controls.commission.value,
      currency,
      0,
      currency,
      this.userBrokers.find(x => x.id === this.controls.broker.value),
    );

    this.stockTransactionsService.postStockTransaction(this.stockTransaction).subscribe(
      success => this.router.navigate(['/' + APP_ROUTES.dashboard]),
      error => this.getErrorMessage(error)
    );
    this.loading = true;
  }
}

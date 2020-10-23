import {Observable} from 'rxjs';

export class AutoCompleteFilter {
  filterField: string;
  filterFuncNames;
  dataSource: (filters) => Observable<any>;
  data: any[];
  searchedValues: string[];
  fetchAllData: boolean;

  public constructor(filterField: string, filterFuncNames, dataSource: (filters) => Observable<any>,
                     fetchAllData = false) {
    this.filterField = filterField;
    this.filterFuncNames = filterFuncNames;
    this.dataSource = dataSource;
    this.data = [];
    this.searchedValues = [''];
    this.fetchAllData = fetchAllData;
    if (fetchAllData) {
      this.fetchData('', '');
    }
  }

  public appendData(data){
    this.data = this.data.concat(data.filter(x => this.data.every(y => y[this.filterField] !== x[this.filterField])));
  }

  public appendSearchedValue(searchedValue: string){
    if (!this.searchedValues.some(x => x === searchedValue)) {
      this.searchedValues.push(searchedValue);
    }
  }

  public getFilterFuncName(filterLength: number) {
    let filterFuncName = this.filterFuncNames[filterLength];
    if (filterFuncName !== '' && filterFuncName !== undefined) {
      filterFuncName = '__' + filterFuncName;
    }
    return filterFuncName;
  }

  public fetchData(filter: string, filterFuncName: string) {
    this.dataSource(`${this.filterField}${filterFuncName}=${filter}`).subscribe(data => {
      this.appendData(data);
    });
  }

  public getFilteredData(filter: string){
    filter = filter.toUpperCase();
    const filterLength = filter.length;
    const filterFuncName = this.getFilterFuncName(filterLength);
    if (!this.fetchAllData && filterFuncName !== undefined && !this.searchedValues.includes(filter)) {
      this.appendSearchedValue(filter);
      this.fetchData(filter, filterFuncName);
    }
    if (!this.data) {
      return [];
    }
    return this.data.filter(x => (x[this.filterField].toUpperCase().startsWith(filter)));
  }

  public dataExists(filter: string) {
    return this.data.some(x => (x[this.filterField].toUpperCase().startsWith(filter)));
  }

  public getValue(filter: string) {
    return this.data.find(x => (x[this.filterField].toUpperCase().startsWith(filter)));
  }
}

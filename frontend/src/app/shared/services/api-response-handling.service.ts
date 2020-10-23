import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ApiResponseHandlingService {
  constructor() {}

  private errorsMap;
  private fieldNamesMap = {
    broker_id: 'broker (id)',
    broker: 'broker',
    company_stock_id: 'company stock (id)',
    company_stock: 'company stock',
    per_stock_price: 'per stock price',
    stock_quantity: 'stock quantity',
    detail: '',
  };

  getAllFieldsErrors(fields) {
    const result = {};

    function recurse(cur, prop) {
      if (Object(cur) !== cur) {
        result[prop] = cur;
      } else if (Array.isArray(cur)) {
        for (let i = 0, l = cur.length; i < l; i++) {
          recurse(cur[i], prop);
          if (l === 0) {
            result[prop] = [];
          }
        }
      } else {
        let isEmpty = true;
        // tslint:disable-next-line: forin
        for (const p in cur) {
          isEmpty = false;
          recurse(cur[p], prop ? prop + '_' + p : p);
        }
        if (isEmpty && prop) {
          result[prop] = {};
        }
      }
    }
    recurse(fields, '');
    return result;
  }

  public getErrorMessage(fields) {
    this.errorsMap = {
      exists: {
        message: 'Data are used: ',
        fields: []
      },
      blank: {
        message: 'Fill in the blank fields: ',
        fields: []
      },
      valid: {
        message: 'Invalid data: ',
        fields: []
      },
      'no more than': {
        message: 'Max data length: ',
        fields: []
      },
      'at least': {
        message: 'Min data length: ',
        fields: []
      },
      required: {
        message: 'Required fields: ',
        fields: []
      },
      'Check provided data': {
        message: 'Check provided data correctness: ',
        fields: []
      },
    };
    const fieldsErrors = this.getAllFieldsErrors(fields);
    for (const fieldKey in fieldsErrors) {
      const error = fieldsErrors[fieldKey];
      const fieldName = fieldKey in this.fieldNamesMap ? this.fieldNamesMap[fieldKey] : fieldKey;
      for (const errorKey in this.errorsMap) {
        if (error.includes(errorKey)) {
          if (errorKey === 'no more than' || errorKey === 'at least') {
            const allowedLength = error.substring(error.lastIndexOf(errorKey) + errorKey.length + 1, error.lastIndexOf('characters'));
            this.errorsMap[errorKey].fields.push(fieldName + ' (' + allowedLength + ')');
          } else {
            this.errorsMap[errorKey].fields.push(fieldName);
          }
        }
      }
    }
    let errorMessage = '';
    // tslint:disable-next-line:forin
    for (const errorKey in this.errorsMap) {
      const key = this.errorsMap[errorKey];
      if (key.fields.length > 0) {
        errorMessage = errorMessage.concat(key.message, key.fields.join(', '), '. ');
      }
    }
    return errorMessage;
  }
}

export interface ILocalFolder {

    name: string;
    path: string;

}

export class LocalFolder implements ILocalFolder {

    public name = '';
    public path = '';

}

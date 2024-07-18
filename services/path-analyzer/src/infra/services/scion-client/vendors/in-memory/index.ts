import { IsdAs } from "src/domain/entities";
import { IScionClient, ShowpathsPathResult } from "src/domain/services";

export class InMemoryScionClient implements IScionClient {
  private store: Map<IsdAs, ShowpathsPathResult[]>;

  constructor(store: Map<IsdAs, ShowpathsPathResult[]> = new Map()) {
    this.store = store;
  }

  async showpaths(destination: IsdAs): Promise<ShowpathsPathResult[]> {
    return this.store.get(destination) ?? [];
  }
}

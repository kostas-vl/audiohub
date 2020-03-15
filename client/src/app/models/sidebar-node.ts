/**
 * This interface exposes properties that define a sidebar navigation node.
 * @export
 * @interface SidebarNode
 */
export interface SidebarNode {

    text: string;
    icon?: string;
    url?: string;
    isHeader: boolean;
    children?: SidebarNode[];

}


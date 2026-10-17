// Facing controls live above Parts in the responsive right inspector.
export async function chooseFacing(page,direction){
 if(!await page.locator('#inspector').isVisible())await page.locator('#toggle-inspector').click();
 await page.locator(`[data-dc-facing="${direction}"]`).click();
}
export async function importHoldFixture(page,state,duration){
 const project=structuredClone((await state()).project);project.directions[project.activeDirection][project.activeFrame].durationMs=duration;
 await page.locator('#br-import').click();await page.locator('#br-text').fill(JSON.stringify(project));await page.locator('#br-apply').click();
}

#include "TCanvas.h"
#include "TROOT.h"
#include "TGraphErrors.h"
#include "TF1.h"
#include "TFitResult.h"
#include "TLegend.h"
#include "TLatex.h"
#include "TArrow.h"


void Draw_graph()
{
	TGraphErrors graph("Threshold_test.txt");
	graph.SetTitle("Threshold scan;Q_{inj} [e^{-}];N_{fired}/N_{inj}");

	graph.SetMarkerStyle(6);
	graph.SetMarkerColor(kBlue);
	graph.SetLineColor(kBlue);

	auto mycanvas = new TCanvas();
	mycanvas->SetGrid();

	graph.DrawClone("APE");
	TF1 f("Electron noise","0.5*(1+erf((x-[0])/(1.414*[1])))",0,1200);
	f.SetLineColor(kRed);
	f.SetLineStyle(1);
	f.SetParameters(700,50);
	f.SetParNames("Threshold","Noise");

	auto fitResPtr=graph.Fit(&f);
	
	f.DrawClone("Same");
	graph.DrawClone("APE");
	graph.GetYaxis()->SetRangeUser(0,1.1);
	graph.DrawClone("APE");

	TLegend leg(.1,.7,.3,.9,"Threshold scan");
	leg.SetFillColor(0);
	graph.SetFillColor(0);
	leg.AddEntry(&graph,"Exp. Points");
	leg.AddEntry(&f,"Error function");
	leg.DrawClone("Same");

	mycanvas->Print("Threshold_graph.pdf");

}

int main(){
	Draw_graph();
	}

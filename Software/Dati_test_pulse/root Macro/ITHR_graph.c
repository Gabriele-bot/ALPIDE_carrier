#include "TCanvas.h"
#include "TROOT.h"
#include "TGraphErrors.h"
#include "TF1.h"
#include "TFitResult.h"
#include "TLegend.h"
#include "TLatex.h"
#include "TArrow.h"


void Draw_graph_ITHR()
{
	TGraphErrors graph("Soglia_ITHR.txt");
	graph.SetTitle("I_{THR} dependency;I_{THR} [pA];Threshold [e^{-}]");

	graph.SetMarkerStyle(6);
	graph.SetMarkerColor(kBlue);
	graph.SetLineColor(kBlue);

	auto mycanvas = new TCanvas();
	mycanvas->SetGrid();

	graph.DrawClone("APE");
	TF1 f("I_{THR} dependency","[0]*x+[1]",0,650);
	f.SetLineColor(kRed);
	f.SetLineStyle(1);
	f.SetParameters(0.7,500);
	f.SetParNames("a","b");

	auto fitResPtr=graph.Fit(&f);
	
	f.DrawClone("Same");
	graph.DrawClone("APE");

	TLegend leg(.1,.7,.3,.9,"I_{THR} dependency");
	leg.SetFillColor(0);
	graph.SetFillColor(0);
	leg.AddEntry(&graph,"Exp. Points");
	leg.AddEntry(&f,"Linear fit");
	leg.DrawClone("Same");


}

int main(){
	Draw_graph_ITHR();
	}

'use strict';

/*
 * Deterministic JavaScript reference for Lab 13: Transformer Language Modeling.
 *
 * This must remain numerically aligned with transformer_language_model_reference.py.
 * It is deliberately a tiny pedagogical decoder-like block, not a pretrained LLM.
 */

const D_MODEL = 4;
const MAX_CONTEXT = 6;
const VOCAB = ['<BOS>','<UNK>','i','like','cats','dogs','sleep','play','.','because','they','run'];
const TOKEN_TO_ID = Object.fromEntries(VOCAB.map((token,index)=>[token,index]));

const TOKEN_EMBEDDINGS = {
  '<BOS>':[0.20,0.00,0.10,0.00], '<UNK>':[0.00,0.10,0.00,0.10],
  i:[0.80,0.10,0.00,0.20], like:[0.20,0.90,0.10,0.00],
  cats:[0.10,0.40,0.90,0.20], dogs:[0.10,0.50,0.70,0.50],
  sleep:[0.00,0.20,0.80,0.90], play:[0.20,0.30,0.70,0.80],
  '.':[0.00,0.10,0.20,0.90], because:[0.30,0.70,0.20,0.10],
  they:[0.70,0.20,0.10,0.40], run:[0.10,0.20,0.60,0.80]
};
const POSITION_VECTORS = [
  [0.00,0.00,0.00,0.00], [0.10,-0.05,0.05,0.00],
  [0.20,0.00,-0.05,0.05], [0.30,0.05,0.00,-0.05],
  [0.40,0.00,0.05,0.00], [0.50,-0.05,0.00,0.05]
];
const W_Q = [[0.80,0.10,0.00,0.00],[0.00,0.70,0.20,0.00],[0.10,0.00,0.80,0.10],[0.00,0.10,0.00,0.90]];
const W_K = [[0.70,0.00,0.20,0.00],[0.10,0.80,0.00,0.00],[0.00,0.10,0.70,0.20],[0.00,0.00,0.20,0.80]];
const W_V = [[0.90,0.00,0.00,0.10],[0.00,0.80,0.10,0.00],[0.10,0.00,0.90,0.00],[0.00,0.10,0.00,0.90]];
const W_FF1 = [[0.60,-0.20,0.10,0.00],[0.10,0.70,-0.10,0.20],[-0.20,0.10,0.60,0.30],[0.00,0.20,0.10,0.70]];
const B_FF1 = [0.00,0.05,0.00,-0.05];
const W_FF2 = [[0.50,0.10,0.00,0.00],[0.00,0.50,0.10,0.00],[0.10,0.00,0.50,0.10],[0.00,0.10,0.00,0.50]];
const B_FF2 = [0,0,0,0];
const W_OUT = [
  [0.10,0.00,0.20,0.10,0.10,0.10,0.00,0.10,0.00,0.20,0.30,0.10],
  [0.00,0.10,0.10,0.30,0.20,0.20,0.10,0.10,0.00,0.30,0.10,0.10],
  [0.00,0.00,0.00,0.10,0.40,0.35,0.35,0.30,0.10,0.10,0.10,0.25],
  [0.00,0.10,0.00,0.00,0.10,0.20,0.45,0.40,0.50,0.00,0.20,0.35]
];
const B_OUT = [-0.30,-0.25,-0.15,-0.05,0.00,0.00,0.05,0.05,0.10,-0.05,-0.05,0.00];

function vecAdd(a,b){ if(a.length!==b.length) throw new Error('vector dimension mismatch'); return a.map((x,i)=>x+b[i]); }
function dot(a,b){ if(a.length!==b.length) throw new Error('dot dimension mismatch'); return a.reduce((s,x,i)=>s+x*b[i],0); }
function rowTimesMatrix(row,matrix){
  if(!matrix.length) return [];
  if(row.length!==matrix.length) throw new Error('row/matrix dimension mismatch');
  const width=matrix[0].length;
  if(matrix.some(row=>row.length!==width)) throw new Error('ragged matrix');
  return Array.from({length:width},(_,j)=>row.reduce((sum,x,i)=>sum+x*matrix[i][j],0));
}
function stableSoftmax(values,temperature=1){
  if(!(temperature>0) || !Number.isFinite(temperature)) throw new Error('temperature must be finite and > 0');
  if(!values.length) return [];
  const scaled=values.map(x=>x/temperature), peak=Math.max(...scaled);
  const exps=scaled.map(x=>Math.exp(x-peak)), denom=exps.reduce((a,b)=>a+b,0);
  return exps.map(x=>x/denom);
}
function entropy(probabilities){ return -probabilities.reduce((sum,p)=>p>0?sum+p*Math.log(p):sum,0); }
function toyTokenize(text,addBos=true){
  const matches=String(text||'').match(/[A-Za-z]+|[.]/g)||[];
  let tokens=matches.map(x=>x.toLowerCase()).map(x=>Object.hasOwn(TOKEN_TO_ID,x)?x:'<UNK>');
  if(addBos) tokens.unshift('<BOS>');
  if(!tokens.length && addBos) tokens=['<BOS>'];
  if(tokens.length>MAX_CONTEXT){
    tokens=tokens.slice(-MAX_CONTEXT);
    if(addBos && tokens[0]!=='<BOS>') tokens=['<BOS>',...tokens.slice(-(MAX_CONTEXT-1))];
  }
  return tokens;
}
function inputVectors(tokens,usePositions=true){
  if(tokens.length>MAX_CONTEXT) throw new Error('context exceeds MAX_CONTEXT');
  return tokens.map((token,i)=>vecAdd(TOKEN_EMBEDDINGS[token]||TOKEN_EMBEDDINGS['<UNK>'],usePositions?POSITION_VECTORS[i]:[0,0,0,0]));
}
function projectRows(rows,matrix){ return rows.map(row=>rowTimesMatrix(row,matrix)); }
function attentionScores(queries,keys){ const scale=Math.sqrt(queries.length?queries[0].length:1); return queries.map(q=>keys.map(k=>dot(q,k)/scale)); }
function applyCausalMask(scores,causalMask=true){ return scores.map((row,i)=>row.map((value,j)=>causalMask&&j>i?null:value)); }
function attentionWeights(maskedScores){
  return maskedScores.map(row=>{
    const probs=stableSoftmax(row.filter(x=>x!==null)); let i=0;
    return row.map(value=>value===null?0:probs[i++]);
  });
}
function weightedValueSum(weights,values){
  if(weights.length!==values.length) throw new Error('weights/value count mismatch');
  if(!values.length) return [];
  return Array.from({length:values[0].length},(_,d)=>weights.reduce((sum,w,i)=>sum+w*values[i][d],0));
}
function feedForward(state){
  const pre=vecAdd(rowTimesMatrix(state,W_FF1),B_FF1), hidden=pre.map(x=>Math.max(0,x));
  return vecAdd(rowTimesMatrix(hidden,W_FF2),B_FF2);
}
function logitsFromState(state){ return vecAdd(rowTimesMatrix(state,W_OUT),B_OUT); }
function forwardTokens(tokens,{usePositions=true,causalMask=true,temperature=1}={}){
  const normalized=tokens.map(token=>Object.hasOwn(TOKEN_TO_ID,token)?token:'<UNK>');
  if(!normalized.length) throw new Error('at least one token is required');
  if(normalized.length>MAX_CONTEXT) throw new Error('context exceeds MAX_CONTEXT');
  const inputs=inputVectors(normalized,usePositions);
  const queries=projectRows(inputs,W_Q), keys=projectRows(inputs,W_K), values=projectRows(inputs,W_V);
  const rawScores=attentionScores(queries,keys), maskedScores=applyCausalMask(rawScores,causalMask), attention=attentionWeights(maskedScores);
  const attentionOutputs=attention.map(row=>weightedValueSum(row,values));
  const residual1=inputs.map((x,i)=>vecAdd(x,attentionOutputs[i]));
  const feedForwardRows=residual1.map(feedForward), finalStates=residual1.map((x,i)=>vecAdd(x,feedForwardRows[i]));
  const logits=logitsFromState(finalStates.at(-1)), probabilities=stableSoftmax(logits,temperature);
  return {tokens:normalized,tokenIds:normalized.map(t=>TOKEN_TO_ID[t]??TOKEN_TO_ID['<UNK>']),inputs,queries,keys,values,rawScores,maskedScores,attention,attentionOutputs,residual1,feedForward:feedForwardRows,finalStates,logits,probabilities,temperature,causalMask,usePositions};
}
function forwardText(text,options={}){ return forwardTokens(toyTokenize(text),options); }
function topTokens(result,n=5){ return VOCAB.map((token,i)=>[token,result.probabilities[i]]).sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])).slice(0,n); }

const API={D_MODEL,MAX_CONTEXT,VOCAB,TOKEN_TO_ID,TOKEN_EMBEDDINGS,POSITION_VECTORS,W_Q,W_K,W_V,W_FF1,B_FF1,W_FF2,B_FF2,W_OUT,B_OUT,vecAdd,dot,rowTimesMatrix,stableSoftmax,entropy,toyTokenize,inputVectors,projectRows,attentionScores,applyCausalMask,attentionWeights,weightedValueSum,feedForward,logitsFromState,forwardTokens,forwardText,topTokens};
if(typeof module!=='undefined'&&module.exports) module.exports=API;
if(typeof window!=='undefined') window.TransformerLanguageModelCore=API;
